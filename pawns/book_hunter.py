import click
import py2neo

from database import neo4j
from utils import logger, query_google_book

log = logger.define_logger('Book Hunter')


def find_node(db, label, node_name):
    """ Find a node in the DB, if not node is found, create.
    A node is identified by label and name

    :param db:
    :param label:
    :param node_name:
    :return: Neo4J node
    """
    node = db.find_one(label, property_key='name', property_value=node_name)
    if node:
        pass
    else:
        log.info('creating new node', extra={'label': label, 'node_name': node_name})
        node = py2neo.Node(label, name=node_name)
        db.create(node)
    return node


def connect_node(db, start_node, end_node, relation_type):
    """ Connect 2 node in the graph DB

    :param db: graph db
    :param start_node:
    :param end_node:
    :param relation_type:
    :return: None
    """
    log.info('Connecting 2 nodes', extra={'start': start_node, 'end': end_node, 'relation': relation_type})
    relationship = py2neo.Relationship(start_node, relation_type, end_node)
    db.create(relationship)


def update_author_book_relation(db, start_node, end_node, relation_type='writes'):
    """ Update author-book relation

    :param db: graph DB
    :param start_node: Author node
    :param end_node: Book node
    :param relation_type:
    :return: None
    """
    relationship = next(db.match(start_node=start_node, end_node=end_node, rel_type=relation_type))

    if relationship is None:
        connect_node(db=db, start_node=start_node, end_node=end_node, relation_type=relation_type)


def find_authors(db):
    """ Find all author in DB

    :param db:
    :return: all author nodes
    """
    return db.run('MATCH (n:Author) RETURN n LIMIT 50')


def crawl_google_book_to_db(db, authors):
    log.info('Crawling Google books to graph database')
    for author in authors:
        author_node = author[0]
        books = query_google_book.query_book_by_author(author=author_node['name'], max_res=20)

        for book in books:
            book_node = find_node(db, 'Book', node_name=book.get('name'))
            connect_node(db, start_node=author_node, end_node=book_node, relation_type='write')


@click.command()
def main():
    db = neo4j.create_connection()
    log.info('Start crawling')
    print(db.run('MATCH (n:Author) RETURN n LIMIT 50').evaluate())
    authors_in_db = find_authors(db)
    crawl_google_book_to_db(db, authors_in_db)


if __name__ == '__main__':
    main()
