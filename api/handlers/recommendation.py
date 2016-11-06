from database import neo4j, config
from utils import logger, query_google_book

log = logger.define_logger('books recommendation')
graph_client = neo4j.SmartGraph(log=log, uri=config.URI)


def on_recommendation_requested(req_body, distance='euclidean'):

    # Parse info from request body
    user_id = req_body.args.get('user_id')

    # Get recommended book, list by based on user's similarity score
    query = "MATCH (u:User)-[d:distance]-(:User)-[r:like]->(b:Book) WHERE u.name='{}' WITH * ORDER BY d.{} RETURN b.name".format(
        user_id, distance)
    recommended_book_records = graph_client.graph.cypher.execute(query)

    # For each book name, parse info from Google Book to construct response
    recommendation_book_list = []

    for item in recommended_book_records:
        book_name = item[0]
        book_info = query_google_book.query_book_by_name(book_name)

        if not book_info:
            continue

        recommendation_book_list.append(book_info[0])

    return {'user_id': user_id,
            'recommendation': recommendation_book_list}
