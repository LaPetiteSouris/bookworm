from py2neo import Graph

from database import config
from utils import logger

log = logger.define_logger('Graph database')


def create_connection(uri):
    log.info('creating neo4j database object')
    return Graph(uri) if uri else Graph(host=config.NEO4J_HOST, port=config.NEO4J_PORT, user=config.NEO4J_USER,
                                        password=config.NEO4J_PWD)
