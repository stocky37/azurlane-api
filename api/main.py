import glob
import json
from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from slugify import slugify
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

from api.pagination import Pagination


class ShipMinified(BaseModel):
    name: str
    slug: str


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


@app.get("/ships", response_model=List[ShipMinified])
def get_ships(pager: Pagination = Depends(Pagination)):
    return pager.paginate(db.all())


@app.get("/ships/{name}")
def get_ship(name: str):
    return db.get(where("slug") == slugify(name))
