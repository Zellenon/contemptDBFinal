from neo4j import GraphDatabase

class Neo4j_Model:
    def __init__(self, url='bolt://localhost:7687', user='neo4j', password='a'):
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
<<<<<<< HEAD
=======

    def getChampSuggestion(self, champ1, champ2, champ3, role1, role2, role3):
        with self.neo4jDriver.session() as session:
            query = "WITH [$champ1, $champ2, $champ3] AS names, [$role1, $role2, $role3] as roles MATCH (m:Champ) <- [r] - (t:Team) - [r2] -> (n:Champ) WHERE n.Name IN names AND NOT m.Name IN names with m,r,t.weight as weight, CASE when (n.Name = names[0] and r2.role = roles[0]) or (n.Name = names[1] and r2.role = roles[1]) or (n.Name = names[2] and r2.role = roles[2]) THEN 1 ELSE 0 END as rolescore return m.Name as Name,sum(weight)+sum(rolescore) as score order by score desc, m.Name LIMIT 2"
        result = session.run(query, champ1 = champ1, champ2 = champ2, champ3 = champ3, role1 = role1, role2 = role2, role3 = role3)
        response = self.makeList(result, "Name")
        print("Response: " + str(response))
        session.close()
        return response

>>>>>>> 754d4119c94ddebca11c003dffccac35bc144cc1
# END CLASS

print(Neo4j_Model().getChampSuggestion("Leblanc", "Nocturne", "Jhin", "support", "buttom", "adc"))
