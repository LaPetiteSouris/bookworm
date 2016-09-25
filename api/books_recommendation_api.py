from flask import request, Blueprint, jsonify

from api.errors.api_exception import NotImplemented
from utils import logger

book_api = Blueprint('book_api', __name__)
log = logger.define_logger('books recommendation api')


@book_api.route('/ping', methods=['GET'])
def index():
    return jsonify({'response': 'pong'}), 200


@book_api.route('/book_list', methods=['POST'])
def send_book_list():
    if request.headers.get('X-Mocking') == 'Enabled':
        log.info('serving mock', extra={'endpoint': '/book_list', 'method': request.method})
        return jsonify({'data_received': True}), 200
    raise NotImplemented('This endpoint has not been implemented', status_code=501)
