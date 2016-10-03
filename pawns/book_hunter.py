import click

from database import neo4j
from utils import logger, query_google_book

log = logger.define_logger('Book Hunter')


def find_authors(db_graph):
    """ Find all author in DB

    :param db_graph:
    :return: all author nodes
    """
    return db_graph.run('MATCH (n:Author) RETURN n LIMIT 50')


def crawl_google_book_to_db(graph_client, authors):
    log.info('Crawling Google books to graph database')
    for author in authors:
        author_node = author[0]
        books = query_google_book.query_book_by_author(author=author_node['name'], max_res=20)

        for book in books:
            book_node = graph_client.find_node('Book', node_name=book.get('name'))
            graph_client.connect_node(start_node=author_node, end_node=book_node, relation_type='write')


@click.command()
def main():
    graph_client = neo4j.SmartGraph(log=log)
    log.info('Start crawling')
    authors_in_db = find_authors(graph_client.graph)
    crawl_google_book_to_db(graph_client, authors_in_db)


if __name__ == '__main__':
    main()
