from pydantic import BaseModel

from .construction import Construction
from .stats import AllStats


class ShipRef(BaseModel):
    name: str
    slug: str


class Ship(ShipRef):
    id: str
    classification: str = None
    construction: Construction = None
    nationality: str = None
    voice_actress: str = None
    stats: AllStats = None
