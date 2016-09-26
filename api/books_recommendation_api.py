from flask import request, Blueprint, jsonify

from api.errors.api_exception import NotImplementedException
from api.mock_response import mock_recommendation
from utils import logger

book_api = Blueprint('book_api', __name__)
log = logger.define_logger('books recommendation api')


@book_api.route('/ping', methods=['GET'])
def index():
    return jsonify({'response': 'pong'}), 200


@book_api.route('/book_list', methods=['POST'])
def send_book_list():
    if request.headers.get('X-Mocking') == 'Enabled':
        log.info('serving mock',
                 extra={'endpoint': '/book_list', 'method': request.method, 'request': str(request.json)})
        return jsonify({'data_received': True}), 200
    raise NotImplementedException('This endpoint has not been implemented', status_code=501)


@book_api.route('/book_feedback', methods=['POST'])
def send_book_feedback():
    if request.headers.get('X-Mocking') == 'Enabled':
        log.info('serving mock',
                 extra={'endpoint': '/feed_back', 'method': request.method, 'request': str(request.json)})
        return jsonify({'data_received': True}), 200
    raise NotImplementedException('This endpoint has not been implemented', status_code=501)


@book_api.route('/book_recommendation', methods=['GET'])
def get_recommended_book():
    if request.headers.get('X-Mocking') == 'Enabled':
        log.info('serving mock',
                 extra={'endpoint': '/book_recommendation', 'method': request.method, 'request': str(request.json)})
        return jsonify(mock_recommendation), 200
    raise NotImplementedException('This endpoint has not been implemented', status_code=501)
