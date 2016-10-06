## Bookworm

Project Bookworm is a book graph-based recommendation engine


## Launching with Docker

```
sudo docker build -t souris/bookworm .
sudo docker run -p 0.0.0.0:3000:3000 bookworm
```


## Populate sample DB
```
CREATE (user1:User {id:'user1'})
CREATE (user2:User {id:'user2'})

CREATE (Jules_Vernes:Author {name:'Jules Vernes'})
CREATE (Around_the_World:Book {name:'Around the world in 80 days'})

CREATE (user1)-[:like {weight:1}]->(Jules_Vernes)
CREATE (user1)-[:like {weight:1}]->(Around_the_World)


CREATE (user2)-[:like {weight:1}]->(Jules_Vernes)
CREATE (user2)-[:like {weight:1}]->(Around_the_World)
```

## Book recommendation query

```
MATCH (u:User)-[d:distance]-(:User)-[r:like]->(b:Book)
WHERE u.id='user1'
WITH *
ORDER BY d.euclidean
RETURN b
```