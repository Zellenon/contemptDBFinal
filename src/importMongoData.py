"""Seperate program. Imports champion & move database into Mongo."""

import sys
from pymongo import MongoClient


def connect():
    """Return a connection to the database."""
    try:
        client = MongoClient("127.0.0.1")
        db = client.CDBFP
        print("Connected succesfully.")
        return db
    except Exception as e:
        print("Could not connect to server.")
        print(e)
        sys.exit(-1)


def getData(fpath):
    """Import a csv file at path csv_name to a mongo colection.

    returns: count of the documants in the new collection
    """
    data = open(fpath).readlines()
    data = [w.replace("\n", "") for w in data]
    data = [w.split(',\t') for w in data]
    headers = data[0]
    print(headers)
    headers[0] = "index"
    entries = [{headers[c]: w[c] for c in range(0, len(headers))}
               for w in data]
    return entries


db = connect()
db.abilities.drop()
db.create_collection("abilities")
# entries = getData("../res/abilities.tsv")
entries = getData("res/abilities.tsv")
db.abilities.insert_many(entries)
db.abilities.create_index([("name", "text"), ("description", "text")])

db.champs.drop()
db.create_collection("champs")
# entries = getData("../res/champs.tsv")
entries = getData("res/champs2.tsv")
db.champs.insert_many(entries)
#db.champs.create_index([("name", "text"), ("title", "text"), ("lore", "text")])
db.champs.create_index([("name", "text"), ("title", "text"), ("lore", "text"), ("tags", "text")])
