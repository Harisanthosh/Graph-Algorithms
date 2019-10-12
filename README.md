# Graph-Algorithms
A comprehensive tutorial on the concepts of graph theory and routing algorithms with practical demonstration on neo4j database

# Pre-requisites

Have a community edition of Neo4j installed and running in your PC

# Create a sample graph

This can be done in the Neo4j interactive browser or in the FAST API Swagger docs in the corresponding POST Method

MERGE (paper0:Paper {name:'Paper 0'})
MERGE (paper1:Paper {name:'Paper 1'})
MERGE (paper2:Paper {name:'Paper 2'})
MERGE (paper3:Paper {name:'Paper 3'})
MERGE (paper4:Paper {name:'Paper 4'})
MERGE (paper5:Paper {name:'Paper 5'})
MERGE (paper6:Paper {name:'Paper 6'})

MERGE (paper1)-[:CITES]->(paper0)

MERGE (paper2)-[:CITES]->(paper0)
MERGE (paper2)-[:CITES]->(paper1)

MERGE (paper3)-[:CITES]->(paper0)
MERGE (paper3)-[:CITES]->(paper1)
MERGE (paper3)-[:CITES]->(paper2)

MERGE (paper4)-[:CITES]->(paper0)
MERGE (paper4)-[:CITES]->(paper1)
MERGE (paper4)-[:CITES]->(paper2)
MERGE (paper4)-[:CITES]->(paper3)

MERGE (paper5)-[:CITES]->(paper1)
MERGE (paper5)-[:CITES]->(paper4)

MERGE (paper6)-[:CITES]->(paper1)
MERGE (paper6)-[:CITES]->(paper4)

# Run the Dashboard and interact with the algorithms

Select the different algorithms from the dropdown and interact with them

