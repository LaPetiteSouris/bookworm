import click
import numpy as np

from database import neo4j
from utils import logger

log = logger.define_logger('Distance Calculator')


def find_users(db_graph):
    """ Find all user in DB

    :param db_graph:
    :return: all user nodes
    """
    return db_graph.run('MATCH (n:User) RETURN n')


def calculate_distance(db_graph, user1, user2):
    query = 'MATCH (u1:User)-[x:like]->(item) , (u1:User)-[x:like]->(item) WHERE u1.name={} AND u2.name={} RETURN x,y'.format(
        str(user1['id']), str(user2['name']))

    result = db_graph.run(query)

    user1_vector = np.array([item[0]['weight'] for item in result])
    user2_vector = np.array([item[1]['weight'] for item in result])

    return np.linalg.norm(user1_vector - user2_vector)


def update_user_distance(graph):
    users = find_users(graph)
    for user in users:
        user_node = user[0]


@click.command()
def main():
    graph_client = neo4j.SmartGraph(log=log)


if __name__ == '__main__':
    main()
