from pymongo import MongoClient
from neo4j import GraphDatabase
import redis

mongoUrl = "mongodb://localhost:27017/pokemon"
neo4jUrl = "bolt://localhost:7687"
neo4jDriver = GraphDatabase.driver(neo4jUrl, auth=('neo4j', 'moderndb'))
redisClient = redis.Redis(port=6379);
batchSize = 200;

def feedSpeciesToNeo4j_heavy (species):
    session = neo4jDriver.session()
    session.run(
        'WITH $species as species '+
        'MERGE (s:species {name: species.name}) '+
        'WITH s, species.pokemons as pokemons '+
        'UNWIND pokemons as poke '+
        'MERGE (p:pokemon {name: poke.pokemon}) '+
        'MERGE (s)-[r:is_species]-(p) '+
        'SET p.weight_kg = poke.weight_kg '+
        'WITH p, poke.type as poketypes '+
        'UNWIND poketypes as typeName '+
        'MERGE (t:type {name: typeName}) '+
        'MERGE (p)-[r:is_type]-(t) '+
        'RETURN p.name as name',
        species=species)
    session.close()

def feedSpeciesToNeo4j (species):
    session = neo4jDriver.session()
    session.run('MERGE (s:species {name: $species})',species=species['name'])
    for pokemon in species['pokemons']:
        session.run(
            'MATCH (s:species {name: $species}) '+
            'MERGE (p:pokemon {name: $pokemon}) '+
            'MERGE (s)-[r:is_species]-(p) ',
            species=species['name'], pokemon=pokemon['pokemon'])
        for type in pokemon['type']:
            session.run ('MATCH (p:pokemon {name: $pokemon}) '+
                'MERGE (t:type {name: $type}) '+
                'MERGE (p)-[r:is_type]-(t) ',
                pokemon=pokemon['pokemon'],type=type)
    session.close()

def feedSpeciesToRedis(species):
    redisClient.set('species:'+species['name'], 1)
    for pokemon in  species['pokemons']:
        redisClient.set('pokemon:'+pokemon['pokemon'], 1);
        for type in pokemon['type']:
            redisClient.set('type:'+type, 1)

def processSpecies(species):
    feedSpeciesToRedis(species)
    #feedSpeciesToNeo4j_heavy(species)
    feedSpeciesToNeo4j(species)

def loadFromMongo ():
    counter=0
    mongoClient = MongoClient (mongoUrl)
    db = mongoClient.pokemon
    cursor = db.pokemon.find({}, batch_size= batchSize)
    print ('Loading data into Neo4j and Redis')
    species = next(cursor, None)
    while species:
        counter+=1
        processSpecies(species)
        species = next(cursor, None)
        if counter%100==0:
            print (str(counter)+' species processed')
    print (str(counter)+' species processed')
    mongoClient.close()



loadFromMongo()
neo4jDriver.close()


