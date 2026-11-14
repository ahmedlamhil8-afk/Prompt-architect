"""
Master Prompt Generator: FastAPI backend (two-agent Claude pipeline)

  Agent 1 (claude-haiku-5-5)  : raw idea  -> strict JSON analysis (forced tool call = schema-valid JSON)
  Agent 2 (claude-sonnet-5-5) : analysis  -> copy-paste-ready Master Prompt

Environment variables
  ANTHROPIC_API_KEY    required
  APP_TOKENS           required, comma-separated valid X-App-Token values (lets you rotate tokens)
  RATE_LIMIT           optional, default "10/minute" (per client IP, applied before auth)
  RATE_LIMIT_STORAGE   optional, e.g. "redis://localhost:6379" (required when running >1 worker)
  ALLOWED_ORIGINS      optional, comma-separated origins for CORS (only if the website is hosted elsewhere)

Website: put index.html next to this file; it is served at "/" (same origin, so no CORS needed).

Run
  pip install -r requirements.txt
  uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers
  (put it behind HTTPS: Caddy / nginx / your cloud load balancer)
"""
import logging
import os
import re
import secrets
import uuid
from pathlib import Path
from typing import Literal, Optional

import anthropic
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
