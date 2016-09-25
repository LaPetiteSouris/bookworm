from py2neo import Graph

from utils import logger

log = logger.define_logger('Graph database')


def create_connection(host, port=7474, username='neo4j', pwd=''):
    log.info('creating neo4j database object')
    return Graph(host=host, port=port, user=username, password=pwd)
