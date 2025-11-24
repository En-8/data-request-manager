from dataclasses import dataclass


@dataclass
class RequestSource:
    """Data transfer object for a request source."""

    id: str
    name: str
