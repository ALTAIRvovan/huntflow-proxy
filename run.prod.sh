#!/bin/bash

venv/bin/python3 -m uvicorn main:app  --host 127.0.0.1 --port 8001 --env-file .env.prod