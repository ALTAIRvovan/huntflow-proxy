#!/bin/bash

venv/bin/python3 -m uvicorn main:app --reload --env-file .env