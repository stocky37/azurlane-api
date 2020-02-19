import glob
import json
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from slugify import slugify
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

from api.models import ShipRef, Ship
from api.pagination import Pagination


def initialise_db():
    tinydb = TinyDB(storage=MemoryStorage)
    for filename in glob.iglob("data/json/ships/*.json"):
        with open(filename, encoding="utf-8") as f:
            tinydb.insert(json.load(f))
    return tinydb


db = initialise_db()
app = FastAPI()


@app.get("/health")
def health():
    return {"healthy": True}


@app.get("/ships", response_model=List[ShipRef])
def get_ships(pager: Pagination = Depends(Pagination)):
    return pager.paginate(db.all())


@app.get("/ships/{name}", response_model=Ship, response_model_exclude_unset=True)
def get_ship(name: str):
    ship = db.get(where("slug") == slugify(name))
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship
