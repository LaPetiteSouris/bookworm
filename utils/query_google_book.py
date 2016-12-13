import os
from time import gmtime, strftime

import requests

GOOGLE_BOOK_API_KEY = os.getenv('GOOGLE_BOOK_API_KEY', 'AIzaSyCeUh088FTqVAQ6Z0PTF1SxyAMqZNJAhx8')
GOOGLE_BOOK_BASE_URL = 'https://www.googleapis.com/books/v1/volumes'


def format_book_result(res):
    volume_info = res.get('volumeInfo')

    return {'name': volume_info.get('title'),
            'author': volume_info.get('authors')[0] if volume_info.get('authors') else None,
            'description': volume_info.get('description'),
            'url': volume_info.get('infoLink'),
            'icon': volume_info.get('imageLinks'),
            'created_at': strftime("%Y-%m-%d %H:%M:%S", gmtime())}


def format_query_params(param):
    """ Replace space with %20 for URL params

    :param param:
    :return:
    """
    return param.replace(' ', '%20')


def query_book_by_author(author, max_res=1):
    """ Send query to Google Book API

    :param author: author's name
    :param max_res: max result to find
    :return: a list of trimmed response
    """
    params ='?q=inauthor:{}&maxResults={}&key={}'.format(format_query_params(author.encode('utf-8')), max_res, GOOGLE_BOOK_API_KEY)
    uri = ''.join([GOOGLE_BOOK_BASE_URL, params])

    res = requests.get(uri)

    return [format_book_result(book) for book in res.json().get('items')] if res.json().get('items') else None


def query_book_by_name(name, max_res=1):
    """ Send query to Google Book API

    :param name: book's name
    :param max_res: max result to find
    :return: a list of trimmed response
    """
    params ='?q=intitle:{}&maxResults={}&key={}'.format(format_query_params(name.encode('utf-8')), max_res, GOOGLE_BOOK_API_KEY)
    uri = ''.join([GOOGLE_BOOK_BASE_URL, params])

    res = requests.get(uri)

    return [format_book_result(book) for book in res.json().get('items')] if res.json().get('items') else None
