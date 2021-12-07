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
    headers[0] = "index"
    entries = [{headers[c]: w[c] for c in range(0, len(headers))}
               for w in data[1:]]
    return entries


db = connect()
db.abilities.drop()
db.create_collection("abilities")
entries = getData("../res/abilities.tsv")
db.abilities.insert_many(entries)
