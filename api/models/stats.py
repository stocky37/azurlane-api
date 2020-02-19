from pydantic import BaseModel


class Stats(BaseModel):
    aa: int
    acc: int
    arm: str
    asw: int
    avi: int
    eva: int
    fp: int
    hp: int
    lck: int
    oil: int
    rld: int


class AllStats(BaseModel):
    base: Stats
    lvl100: Stats
    lvl120: Stats
    lvl100Retro: Stats = None
    lvl120Retro: Stats = None
