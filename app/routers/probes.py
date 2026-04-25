from fastapi import APIRouter

from app.schemas.probe import LaunchProbeRequest, ProbeResponse
from app.services import probe_service

router = APIRouter()


@router.post("", response_model=ProbeResponse, status_code=201)
def launch_probe(body: LaunchProbeRequest) -> ProbeResponse:
    """Launch a probe onto the plateau at position (0, 0)."""
    probe = probe_service.launch_probe(body.x, body.y, body.direction)
    return ProbeResponse(id=probe.id, x=probe.x, y=probe.y, direction=probe.direction)
