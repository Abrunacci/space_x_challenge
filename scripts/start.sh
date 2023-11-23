#! /bin/bash
set -e

echo 'Starting app...'
uvicorn src.main:app --reload --host ${API_HOST} --log-level ${LOG_LEVEL}