from fastapi import APIRouter, HTTPException

from app.schemas.probe import LaunchProbeRequest, MoveProbeRequest, ProbeResponse
from app.services import probe_service

router = APIRouter()


@router.post("", response_model=ProbeResponse, status_code=201)
def launch_probe(body: LaunchProbeRequest) -> ProbeResponse:
    """Launch a probe onto the plateau at position (0, 0)."""
    probe = probe_service.launch_probe(body.x, body.y, body.direction)
    return ProbeResponse(id=probe.id, x=probe.x, y=probe.y, direction=probe.direction)


@router.post("/{probe_id}/commands", response_model=ProbeResponse)
def move_probe(probe_id: str, body: MoveProbeRequest) -> ProbeResponse:
    """Send movement commands to an existing probe."""
    probe = probe_service.get_probe(probe_id)
    if probe is None:
        raise HTTPException(status_code=404, detail="Probe not found.")
    try:
        probe = probe_service.move_probe(probe, body.commands)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return ProbeResponse(id=probe.id, x=probe.x, y=probe.y, direction=probe.direction)
