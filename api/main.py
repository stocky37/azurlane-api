import glob
import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from slugify import slugify
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"healthy": True}


@app.get("/ships", response_model=List[ShipMinified])
def get_ships():
    return db.all()


@app.get("/ships/{name}")
def get_ship(name: str):
    return db.get(where("slug") == slugify(name))
