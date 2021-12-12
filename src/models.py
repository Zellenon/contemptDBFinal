from pymongo import MongoClient
from neo4j import GraphDatabase
import redis


class Neo4jModel:
    def __init__(self, url='bolt://localhost:7687', user='neo4j', password='moderndb'):
        self.neo4jUrl = url;
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.neo4jDriver.close()

    #This function is used to make a list with the neo4j results (only lists the selected attribute)
    def makeList(self, results, attribute='name'):
        results_as_list = []
        if results.peek():
            listResult = list(results)
            for record in listResult:
                results_as_list.append(record[attribute])
        return results_as_list


    def getSpeciesSuggestions(self, speciesName):
        with self.neo4jDriver.session() as session:
            query = "MATCH (s1:species {name: $speciesName})-[:is_species]-(p:pokemon)-[:is_type]-(t:type)-[:is_type]-(" \
                    "q:pokemon)-[:is_species]-(s2:species) WHERE s1.name<>s2.name AND p.name<>q.name RETURN DISTINCT " \
                    "s2.name as name LIMIT 5 "
            result = session.run(query,speciesName=speciesName)
            response = self.makeList(result, "name")
            session.close()
            return response

    def getPokemonSuggestions(self, pokemonName):
        with self.neo4jDriver.session() as session:
            query = "MATCH (p:pokemon{name: $pokemonName})-[:is_type]-(t:type)-[:is_type]-(r:pokemon) WHERE "\
                                 "p.name<>r.name RETURN DISTINCT r.name as name LIMIT 10"
            result = session.run(query,pokemonName=pokemonName)
            response = self.makeList(result, "name")
            session.close()
            return response


class RedisModel:
    def __init__(self, port=6379):
        self.redisClient = redis.Redis(port=port)

    def searchKeys(self, text, type):
        print(text)
        searchKey = type + text + "*"
        keys = self.redisClient.keys(searchKey)
        return keys

    def searchSpecies(self, param):
        keys = self.searchKeys(param, "species:");
        results = []
        for key in keys:
            key = key.decode().replace("species:", "")
            results.append(key)
        return results


class MongoModel:
    def __init__(self, url='mongodb://localhost:27017/pokemon'):
        self.mongoUrl = url
        self.mongoClient = MongoClient(url)

    def close(self):
        self.mongoClient.close()

    def getSpecies(self, name):
        db = self.mongoClient.pokemon
        result = db.pokemon.find({'name': name})
        if not result:
            result = {"name": "Data NOT found", "name": name}
        return list(result)

    def getPokemon(self, name):
        db = self.mongoClient.pokemon
        result = db.pokemon.find({'pokemons.pokemon': name}, {'name': 1, 'pokemons.$': 1})
        if not result:
            result = {"name": "Data NOT found", "name": name}
        return list(result)

