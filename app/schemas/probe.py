from pydantic import BaseModel, Field

from app.models.probe import Direction


class LaunchProbeRequest(BaseModel):
    """Payload to launch a probe and define the plateau boundaries."""

    x: int = Field(..., gt=0, description="X coordinate of the plateau upper-right corner")
    y: int = Field(..., gt=0, description="Y coordinate of the plateau upper-right corner")
    direction: Direction = Field(..., description="Initial direction the probe faces")


class ProbeResponse(BaseModel):
    """Representation of a probe returned by the API."""

    id: str
    x: int
    y: int
    direction: Direction
