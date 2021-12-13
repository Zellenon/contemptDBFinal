"""Seperate program. Imports match & move database into neo4j."""

from py2neo import Graph
from pprint import pprint
import operator
import sys


def connect():
    """Return a connection to the database."""
    try:
        creds = open("../res/credentials.txt").read()[:-1]
        print(creds)
        graph = Graph(password=creds)
        print("connected.")
        return graph
    except Exception as e:
        print("Could not connect to server.")
        print(e)
        sys.exit(-1)


db = connect()
data = open("../res/matchdata2.csv").readlines()
data = [w[:-1] for w in data]
data = [w.split(',') for w in data]
# pprint(data)
# print(data[0])
blueindices = [1, 3, 4, 5, 6, 7, 0]
redindices = [2, 8, 9, 10, 11, 12, 0]

# blueMatches = [[
#     v for v in w if operator.indexOf(w, v) in blueindices]
#                for w in data[1:]]
blueMatches = [[w[v] for v in blueindices] for w in data[1:]]
# blueMatches = blueMatches[1:] + blueMatches[:1]
# redMatches = [[
#     v for v in w if operator.indexOf(w, v) in redindices]
#                for w in data[1:]]
# redMatches = redMatches[1:] + redMatches[:1]
redMatches = [[w[v] for v in redindices] for w in data[1:]]

matches = blueMatches + redMatches
# for match in matches:
    # match[0] = match[0] == '1'
# pprint(matches)

print("Matches Collated.")

champs = []
for match in matches:
    for ch in match[1:-1]:
        champs.append(ch)

champs = set(champs)
# pprint(champs)

for champ in champs:
    db.run("MERGE (c: Champ {Name: \"" + champ + "\"})")

print("Champs Imported.")

for match in matches:
    print(match)
    st = ("MATCH (top: Champ {Name: \"" + match[1] + "\"}), " +
          "(jungle: Champ {Name: \"" + match[2] + "\"}), " +
          "(mid: Champ {Name: \"" + match[3] + "\"})," +
          "(adc: Champ {Name: \"" + match[4] + "\"})," +
          "(bottom: Champ {Name: \"" + match[5] + "\"})\n")
    st += ("MERGE (t: Team {matchNum: " + str(int(match[6])) +
           ", weight: " + str(int(match[0])*2-1) + "}) "
           "MERGE (t)-[r1:IN_PARTY {role:'top'}]->(top) "
           "MERGE (t)-[r2:IN_PARTY {role:'jungle'}]->(jungle) "
           "MERGE (t)-[r3:IN_PARTY {role:'mid'}]->(mid) "
           "MERGE (t)-[r4:IN_PARTY {role:'adc'}]->(adc) "
           "MERGE (t)-[r5:IN_PARTY {role:'bottom'}]->(bottom)")
    db.run(st)

print("Matches Imported.")
