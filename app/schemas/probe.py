from pydantic import BaseModel, Field

from app.models.probe import Direction


class MoveProbeRequest(BaseModel):
    """Payload to send movement commands to a probe."""

    commands: str = Field(
        ...,
        pattern=r"^[MLR]+$",
        description="Sequence of commands: M (move), L (turn left), R (turn right)",
    )


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


class ProbeListResponse(BaseModel):
    """List of all probes currently deployed on the plateau."""

    probes: list[ProbeResponse]
