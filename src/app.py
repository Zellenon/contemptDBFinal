from flask import Flask, request, jsonify, render_template
from models import MongoModel, RedisModel, Neo4jModel
from mongoModel import Mongo_Model
from neoModel import Neo4j_Model

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

@app.route("/champs", methods=["GET"])
def listSpecies(speciesName=None):
    if not (speciesName):
        speciesName = request.args.get("name")

    mongoDoc = Mongo_Model().getChamps(speciesName)
    # neoResults = Neo4jModel().getSpeciesSuggestions(speciesName)

    champs = []
    for champ in mongoDoc:
        champs.append({"name": champ['name'], "title": champ['title'], "lore": champ['lore'], "tags": champ['tags'], "image": "/static/portraits/" + champ["index"] + ".jpg"})

    print(mongoDoc)

    template = render_template("champs.html", champions=champs)
    return template

@app.route("/recs", methods=["GET"])
def listRecs(champ1=None, champ2=None, champ3=None):
    if not (champ1):
        champ1=request.args.get("champ1")
    if not (champ2):
        champ2=request.args.get("champ2")
    if not (champ3):
        champ3=request.args.get("champ3")

    neoDoc = Neo4j_Model().getChampRandFiltered(champ1, champ2, champ3)
    print("NeoDoc = " + str(neoDoc))
    print("NeoDoc Type = " + str(type(neoDoc)))
    print("NeoDoc length = " + str(len(neoDoc)))
    print("NeoDoc1: " + neoDoc[0])
    print("NeoDoc2: " + neoDoc[1])


    championOne = Mongo_Model().getChamps(neoDoc[0])[0]
    print("Champion1: " + str(championOne))
    championTwo = Mongo_Model().getChamps(neoDoc[1])[0]
    print("champion2: " + str(championTwo))

    template = render_template("recs.html", rec1=championOne, rec2=championTwo)
    return template

# @app.route("/champs")
# def champs():

#     return render_template("champs.html", champName="Olaf")

if __name__ == "__main__":
    app.run( host='127.0.0.1', port=8000)                    # run the flask app
    #app.run(debug=True, host='127.0.0.1',
    #        port=8888)  # in debug mode the server restarts if code is added to the Application
