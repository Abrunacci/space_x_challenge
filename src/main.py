"""src/main.py
FastAPI initialization
"""
import logging.config

from fastapi import FastAPI


ROUTERS = []

app = FastAPI()

logging.config.fileConfig("/app/src/logging.conf", disable_existing_loggers=False)

log = logging.getLogger(__name__)

for router in ROUTERS:
    app.include_router(
        router,
    )
