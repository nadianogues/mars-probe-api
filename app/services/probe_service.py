from app.models.probe import Direction, Plateau, Probe

_probes: dict[str, Probe] = {}


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
