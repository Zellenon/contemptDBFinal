from pymongo import MongoClient
import redis
import re #regular expressions
import json

#keep track of how many pokemon we have processed
processedpokemon = 0
#The name of the mongo database
mongoDBDatabase = 'pokemon'
mongoCollection = 'pokemon'
mongoUrl = "mongodb://localhost:27017/pokemon"

#The size of document upload batches
batchSize = 50

  
#database clients
redisClient = redis.Redis(port=6379, decode_responses=True)


## A helper function that builds a good mongoDB key
## @param string the unicode string being keyified
def mongoKeyify(string):
  # remove bad chars, and disallow starting with an underscore
#  string = re.sub("[\t \?\#\\\-\+\.\,'\"()*&!\/]+", '_', string)
    s = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,\ ]", "_", string.lower())
    return re.sub("^_+", '', s)

                          
## Insert documents into mongoDB in bulk.
## @param documents The documents to store
## @param count The number of documents being inserted.
def saveDocs(documents, count):
    with MongoClient(mongoUrl) as client:
        dbo = client[mongoDBDatabase]
        res = dbo[mongoCollection].insert_many(documents)
        print("Number of documents inserted: " + str(len(res.inserted_ids)))  
    
#  * Loop through all of the pokemon populated in Redis. We expect
#  * the format of each key to be 'species:pokemon Name' having the value
#  * as a set with all the pokemon properties. The pokemons each have
#  * the list of types, keyed by 'pokemon:specie Name:pokemon Name'.
#  * The pokemon name, set of pokemon properties, and pokemon type(s)
#  * populates the mongoDB documents. eg:
#  {
#      "_id" : "Seed_Pokémon",
#      "name" : "Seed Pokémon",
#      "pokemons" : [
#          {
#              "pokedexNumber" : "2",
#              "pokemon" : "Ivysaur",
#              "height_m" : "1.0",
#              "weight_kg" : "13.0",
#              "type" : [
#                  "Poison",
#                  "Grass"
#              ]
#          },
#          {
#              "pokedexNumber" : "1",
#              "pokemon" : "Bulbasaur",
#              "height_m" : "0.7",
#              "weight_kg" : "6.9",
#              "type" : [
#                  "Poison",
#                  "Grass"
#              ]
#          }
#      ]
#  }
#  */
                          
def populatepokemon():
    readSpecies = 0
    speciesBatch = []
    for speciesKey in redisClient.keys('species:*'):
        #substring of 'pokemon:'.length gives us the pokemon species name
        speciesName = speciesKey[8:]
        pokemonDocs =[]
        for pokemon in redisClient.smembers(speciesKey):
            #for pokemon in pokemons:
            pokemonDoc = json.loads(pokemon)
            pokemonName = pokemonDoc['pokemon']
            pokemonDoc["type"] = []
            for types in redisClient.smembers("pokemon:"+speciesName+":"+pokemonName):  
                pokemonDoc['type'].append(types)
            pokemonDocs.append(pokemonDoc)
          
        #add this new species document to the batch to be executed later
        speciesBatch.append({
            "_id": mongoKeyify(speciesName),
            "name": speciesName,
            "pokemons": pokemonDocs})
        #keep track of the total number of species read
        readSpecies+=1

        #upload batches of 50 values to mongodb 
        if (len(speciesBatch) >= batchSize):
            saveDocs(speciesBatch, len(speciesBatch))
            #empty out the batch array to be filled again
            speciesBatch = [];              

        if (readSpecies %100 == 0):
            print ('species Loaded: ' + str(readSpecies))
        
    #upload to mongodb the remaining values left
    if (len(speciesBatch) > 0):
        saveDocs(speciesBatch, len(speciesBatch))
        
    print ('species Loaded: ' + str(readSpecies))
    
        
populatepokemon()
redisClient.quit()