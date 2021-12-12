import redis
import csv
import json

# Redis client
redisClient = redis.Redis(port=6379);

# The CSV file containing the pokemon data
csvFilename = "pokedex_(Update_05.20).csv"
# Track how many file lines we've processed
processedLines = 0


## This function loops through the
## CSV data file and populates Redis
def populateRedis():
    line_count = 0
    with open(csvFilename, encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for data in csv_reader:
            species = data['species']
            pokemon = data['name']

            pokemonObj = {
                "pokedexNumber": data['pokedex_number'],
                "pokemon": data['name'],
                "height_m": data['height_m'],
                "weight_kg": data['weight_kg']
            }
    
    
            line_count += 1
            if line_count%100 == 0:
                print(f'Processed {line_count} lines.')
    
            redisClient.sadd('species:' + species, json.dumps(pokemonObj))
            type_1 = data['type_1']
            type_2 = data['type_2']
            if type_1 != '':
                redisClient.sadd("pokemon:"+species+":"+pokemon, type_1);
            if type_2 != '':
                redisClient.sadd("pokemon:"+species+":"+pokemon, type_2);         
    print(f'Processed {line_count} lines.')


populateRedis();
redisClient.quit();
