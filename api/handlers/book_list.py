from database import neo4j, config
from utils import logger

log = logger.define_logger('books list request handler')
graph = neo4j.SmartGraph(log=log, uri=config.URI)


def on_book_list_requested(req_body):
    # Parse info from request body
    user_id = req_body.json.get('user_id')
    book_list = req_body.json.get('books')

    for book in book_list:
        title = book.get('name')
        author = book.get('author')

        # Get node from node's name
        user_node = graph.find_node(label='User', node_name=user_id)
        book_node = graph.find_node(label='Book', node_name=title)
        author_node = graph.find_node(label='Author', node_name=author)

        # Update relation between user and book
        user_book_rel = graph.create_relation(user_node, book_node, relation_type='like')
        graph.update_relation_props(user_book_rel, {'weight': 1})

        # Update relation between user and author, +1 in the weight if user like one book written by this author
        user_author_rel = graph.create_relation(user_node, author_node, relation_type='like')
        # Increment weighted like between author and user
        weight = user_author_rel.properties.get('weight', 0)
        graph.update_relation_props(user_author_rel, {'weight': weight + 1})
