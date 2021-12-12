from flask import Flask, request, jsonify, render_template
from models import MongoModel, RedisModel, Neo4jModel
from mongoModel import Mongo_Model

app = Flask(__name__)

#Templates need to be in a templates folder
@app.route("/")
def hello():
    return render_template("template.html")


@app.route("/search", methods=["GET"])
def autocompleteSpecies():
    term = request.args.get("term")
    result = RedisModel().searchSpecies(term)
    return jsonify(result)


# @app.route("/species", methods=["GET"])
# def listSpecies(speciesName=None):
#     if not (speciesName):
#         speciesName = request.args.get("name")

#     mongoDoc = MongoModel().getSpecies(speciesName)[0]
#     pokemon = []
#     if mongoDoc and mongoDoc['pokemons']:
#         for poke in mongoDoc['pokemons']:
#             pokemon.append({"name": poke['pokemon'], "type": poke['type']})

#     neoResults = Neo4jModel().getSpeciesSuggestions(speciesName)
#     template = render_template("species.html", speciesName=speciesName, pokemons=pokemon, speciessug=neoResults)
#     return template

@app.route("/champs", methods=["GET"])
def listSpecies(speciesName=None):
    if not (speciesName):
        speciesName = request.args.get("name")

    mongoDoc = Mongo_Model().getChamps(speciesName)
    neoResults = Neo4jModel().getSpeciesSuggestions(speciesName)

    print(mongoDoc)
    name = mongoDoc[0]['name']
    title = mongoDoc[0]['title']
    lore = mongoDoc[0]['lore']

    template = render_template("champs.html", champName=name, champTitle=title, champLore=lore)
    return template

@app.route("/pokemon", methods=["GET"])
def listPokemon(pokemonName=None):
    if not (pokemonName):
        pokemonName = request.args.get("name")

    mongoDoc = MongoModel().getPokemon(pokemonName)[0]
    pokemonDoc = mongoDoc["pokemons"][0]
    speciesName = mongoDoc["name"]

    neoResults = Neo4jModel().getPokemonSuggestions(pokemonName)

    template = render_template("pokemons.html", speciesName=speciesName, pokemonName=pokemonName, pokemons=neoResults,
                               type=pokemonDoc['type'], weight=pokemonDoc["weight_kg"], height=pokemonDoc["height_m"])
    return template

# @app.route("/champs")
# def champs():

#     return render_template("champs.html", champName="Olaf")

if __name__ == "__main__":
    app.run( host='127.0.0.1', port=8000)                    # run the flask app
    #app.run(debug=True, host='127.0.0.1',
    #        port=8888)  # in debug mode the server restarts if code is added to the Application
