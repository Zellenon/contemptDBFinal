from neo4j import GraphDatabase

class Neo4j_Model:
    def __init__(self, url='bolt://localhost:7687', user='neo4j', password='moderndb'):
        self.neo4jUrl = url
        self.neo4jDriver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.neo4jDriver.close()

    #This function is used to make a list with the neo4j results (only lists the selected attribute)
    def makeList(self, results, attribute='Name'):
        results_as_list = []
        if results.peek():
            listResult = list(results)
            for record in listResult:
                results_as_list.append(record[attribute])
        return results_as_list

    # Any two champs, doesn't need input
    def getChampSuggestionsRand(self, champName = ""):
        with self.neo4jDriver.session() as session:
            query = "MATCH (n:Champ) WHERE n.Name <> $champName RETURN DISTINCT n.Name as Name LIMIT 2"
        result = session.run(query, champName = champName)
        response = self.makeList(result, "Name")
        session.close()
        return response

    # Any two champs, but needs three champ string inputs (can be empty string)
    def getChampRandFiltered(self, champ1, champ2, champ3):
        with self.neo4jDriver.session() as session:
            query = "MATCH (n:Champ) WHERE n.Name <> $champ1 AND n.Name <> $champ2 AND n.Name <> $champ3 RETURN DISTINCT n.Name as Name LIMIT 2"
        result = session.run(query, champ1 = champ1, champ2 = champ2, champ3 = champ3)
        response = self.makeList(result, "Name")
        print("Response: " + str(response))
        session.close()
        return response
# END CLASS

print(Neo4j_Model().getChampRandFiltered("Caitlyn", "Swain", "Bard"))
