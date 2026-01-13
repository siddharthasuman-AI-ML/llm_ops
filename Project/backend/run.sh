#!/bin/bash
echo "Starting SLM Training Platform API..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
