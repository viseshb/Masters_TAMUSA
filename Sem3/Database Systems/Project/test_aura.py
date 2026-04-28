from py2neo import Graph

# Aura connection details
AURA_URI = "neo4j+s://4259b476.databases.neo4j.io"
AURA_USER = "neo4j"
AURA_PASSWORD = "ZeiddFrukfPm9k3u3jnv4FvNLSV-8yLqfpMxZM2eUHg"

graph = Graph(AURA_URI, auth=(AURA_USER, AURA_PASSWORD))
result = graph.run("RETURN 'Connected to Neo4j Aura successfully!' AS message").data()
print(result)
