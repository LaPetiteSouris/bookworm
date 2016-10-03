import py2neo

from database import config


class SmartGraph:
    def __init__(self, log, uri=None):
        self.graph = py2neo.Graph(uri) if uri else py2neo.Graph(host=config.NEO4J_HOST, port=config.NEO4J_PORT,
                                                                user=config.NEO4J_USER,
                                                                password=config.NEO4J_PWD)
        self.log = log

    def find_node(self, label, node_name):
        """ Find a node in the graph, if not node is found, create.
        A node is identified by label and name

        :param label:
        :param node_name:
        :return: Neo4J node
        """
        node = self.graph.find_one(label, property_key='name', property_value=node_name)
        if node:
            pass
        else:
            self.log.info('creating new node', extra={'label': label, 'node_name': node_name})
            node = py2neo.Node(label, name=node_name)
            self.graph.create(node)
        return node

    def connect_node(self, start_node, end_node, relation_type):

        """ Connect 2 node in the graph
        :param start_node:
        :param end_node:
        :param relation_type:
        :return: None
        """
        self.log.info('Connecting 2 nodes', extra={'start': start_node, 'end': end_node, 'relation': relation_type})
        relationship = py2neo.Relationship(start_node, relation_type, end_node)
        self.graph.create(relationship)

    def update_relation(self, start_node, end_node, relation_type='writes'):

        """ Update author-book relation

        :param start_node: Author node
        :param end_node: Book node
        :param relation_type:
        :return: None
        """
        relationship = next(self.graph.match(start_node=start_node, end_node=end_node, rel_type=relation_type))

        if relationship is None:
            self.connect_node(start_node=start_node, end_node=end_node, relation_type=relation_type)
