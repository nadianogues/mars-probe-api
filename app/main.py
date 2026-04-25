from fastapi import FastAPI

from app.routers import probes

app = FastAPI(title="Mars Probe API")

app.include_router(probes.router, prefix="/probes", tags=["probes"])
