from pymongo import MongoClient

class Mongo_Model:
    def __init__(self, url='mongodb://localhost:27017/pokemon'):
        self.mongoUrl = url
        self.mongoClient = MongoClient(url)

    def close(self):
        self.mongoClient.close()

    def getChamps(self, term):
        db = self.mongoClient.CDBFP
        result = db.champs.find({ "$text": { "$search": term}}, {"index" : 1, "name": 1, "title": 1, "lore": 1, "tags": 1, "_id": 0})
        # print("Result: " + str(list(result)))
        # print("NumResults: " + str(len(list(result))))
        if not result:
            result = {"name": "Champ NOT found", "name": term}
        return list(result)

    def getChampByID(self, id):
        db = self.mongoClient.CDBFP
        result = db.champs.find({'id': id})
        if not result:
            result = {"name": "Champ NOT found", "name": id}
        return list(result)

    def getAbilities(self, term):
        db = self.mongoClient.CDBFP
        result = db.abilities.find({ "$text": { "$search": term}}, {"index" : 1, "champion": 1, "name": 1, "description": 1, "_id": 0})
        if not result:
            result = {"name": "Ability NOT found", "search": term}
        return list(result)

    def getAbilitiesFromChamp(self, champID):
        db = self.mongoClient.CDBFP
        result = db.abilities.find({"champion" : champID})
        if not result:
            result = {"name": "Abilities NOT found", "search": champID}
        return list(result)

# END CLASS

def listAbilities(term=None):
    if not (term):
        return None

    mongoDoc = Mongo_Model().getAbilities(term)
    abilities = []
    if mongoDoc:
        for ability in mongoDoc:
            #abilities.append({"name": ability['name'], "description": ability['description']})
            abilities.append({"name": ability['name']})
    return abilities

def listAbilitiesFromChamp(champID=None):
    if not (champID):
        return None

    mongoDoc = Mongo_Model().getAbilitiesFromChamp(champID)
    abilities = []
    if mongoDoc:
        for ability in mongoDoc:
            #abilities.append({"name": ability['name'], "description": ability['description']})
            abilities.append({"name": ability['name']})
    return abilities

def listChamps(term=None):
    if not (term):
        return None

    mongoDoc = Mongo_Model().getChamps(term)
    champs = []
    if mongoDoc:
        for champ in mongoDoc:
            #champs.append({"name": champ['name'], "tags": champ['tags'], "lore": champ['lore'], "title": champ[title]})
            champs.append({"name": champ['name'], "tags": champ['tags']})
    return champs    


Mongo_Model().close()