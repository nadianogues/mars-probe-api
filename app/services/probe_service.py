from app.models.probe import Direction, Plateau, Probe

_probes: dict[str, Probe] = {}

_TURN_LEFT: dict[Direction, Direction] = {
    Direction.NORTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
}

_TURN_RIGHT: dict[Direction, Direction] = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
}

_MOVE_DELTA: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0),
}


def launch_probe(max_x: int, max_y: int, direction: Direction) -> Probe:
    """Create a new probe at position (0, 0) on a plateau defined by (max_x, max_y).

    Args:
        max_x: X coordinate of the plateau upper-right corner.
        max_y: Y coordinate of the plateau upper-right corner.
        direction: Initial cardinal direction the probe faces.

    Returns:
        The newly created Probe instance stored in memory.
    """
    plateau = Plateau(max_x=max_x, max_y=max_y)
    probe = Probe(x=0, y=0, direction=direction, plateau=plateau)
    _probes[probe.id] = probe
    return probe


def get_probe(probe_id: str) -> Probe | None:
    """Retrieve a probe by its unique identifier.

    Args:
        probe_id: The probe's unique identifier.

    Returns:
        The Probe instance if found, otherwise None.
    """
    return _probes.get(probe_id)


def list_probes() -> list[Probe]:
    """Return all probes currently stored in memory."""
    return list(_probes.values())


def move_probe(probe: Probe, commands: str) -> Probe:
    """Execute a sequence of movement commands on a probe.

    The entire sequence is validated before any movement is applied.
    If any command would move the probe out of the plateau bounds,
    no command is executed and a ValueError is raised.

    Args:
        probe: The probe to move.
        commands: A string of commands composed of 'M', 'L' and 'R'.

    Returns:
        The updated Probe instance.

    Raises:
        ValueError: If any 'M' command would take the probe out of bounds.
    """
    x, y, direction = probe.x, probe.y, probe.direction

    for command in commands:
        if command == "L":
            direction = _TURN_LEFT[direction]
        elif command == "R":
            direction = _TURN_RIGHT[direction]
        elif command == "M":
            dx, dy = _MOVE_DELTA[direction]
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x <= probe.plateau.max_x and 0 <= new_y <= probe.plateau.max_y):
                raise ValueError(
                    f"Command 'M' at ({x}, {y}) facing {direction.value} "
                    f"would move the probe out of the plateau bounds."
                )
            x, y = new_x, new_y

    probe.x, probe.y, probe.direction = x, y, direction
    return probe
