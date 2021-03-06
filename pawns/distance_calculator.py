import itertools

import numpy as np

from database import neo4j, config
from utils import logger

log = logger.define_logger('Distance Calculator')


def find_users(db_graph):
    """ Find all user in DB

    :param db_graph:
    :return: all user nodes
    """
    return db_graph.cypher.execute('MATCH (n:User) RETURN n')


def calculate_distance(db_graph, user1, user2):
    query = "MATCH (u1:User)-[x:like]->(item) , (u2:User)-[y:like]->(item) WHERE u1.name='{}' AND u2.name='{}' RETURN x,y".format(
        str(user1['name']), str(user2['name']))

    result = list(db_graph.cypher.execute(query))

    user1_vector = np.array([item[0]['weight'] for item in result])
    user2_vector = np.array([item[1]['weight'] for item in result])

    return np.linalg.norm(user1_vector - user2_vector)


def update_user_distance(graph, user_list):
    user_node_list = [user[0] for user in user_list]

    for user1, user2 in itertools.combinations(user_node_list, 2):
        dist = calculate_distance(graph.graph, user1, user2)
        relation = graph.create_relation(user1, user2, 'distance')
        log.info('updating user distance', extra={'user_1': user1, 'user_2': user2})
        graph.update_relation_props(relation, {'euclidean': dist})


def launch():
    graph_client = neo4j.SmartGraph(log=log, uri=config.URI)
    user_list = find_users(graph_client.graph)
    update_user_distance(graph_client, user_list)


launch()
