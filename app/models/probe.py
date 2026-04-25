import uuid
from dataclasses import dataclass, field
from enum import Enum


class Direction(str, Enum):
    """Cardinal directions a probe can face."""

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


@dataclass
class Plateau:
    """Rectangular plateau on Mars defined by its upper-right corner."""

    max_x: int
    max_y: int


@dataclass
class Probe:
    """A probe deployed on the Martian plateau."""

    x: int
    y: int
    direction: Direction
    plateau: Plateau
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
