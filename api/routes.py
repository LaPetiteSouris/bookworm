from flask import request, Blueprint, jsonify, g

from api.errors.api_exception import UnauthorizedException
from api.handlers import feedback, recommendation, user_auth, book_list
from api.mock_response import mock_recommendation
from utils import logger

book_api = Blueprint('book_api', __name__)
log = logger.define_logger('books recommendation api')


@book_api.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    return response


@book_api.route('/ping', methods=['GET'])
def index():
    return jsonify({'response': 'pong'}), 200


@book_api.route('/signup', methods=['POST'])
def signup():
    user_id = user_auth.on_user_signup(request)

    if not user_id:
        raise UnauthorizedException('User already exists', status_code=401)

    return jsonify({'user_created': True, 'user_id': user_id}), 200


@book_api.route('/login', methods=['POST'])
def login():
    user_id = user_auth.on_user_auth_request(request)

    if user_id:
        return jsonify({'user_authenticated': True, 'user_id': user_id}), 200

    raise UnauthorizedException('User not authorized', status_code=403)


@book_api.route('/book_list', methods=['POST'])
def send_book_list():
    log.info('serving data',
             extra={'endpoint': '/book_list', 'method': request.method, 'request': str(request.json)})
    book_list.on_book_list_requested(request)

    return jsonify({'data_received': True}), 200


@book_api.route('/book_feedback', methods=['POST'])
def send_book_feedback():
    # Mock response
    if request.headers.get('X-Mocking') == 'Enabled':
        log.info('serving mock',
                 extra={'endpoint': '/feed_back', 'method': request.method, 'request': str(request.json)})
        return jsonify({'data_received': True}), 200

    # correctly implemented response
    log.info('serving test response',
             extra={'endpoint': '/feed_back', 'method': request.method, 'request': str(request.json)})
    feedback.on_like_click(request.json)

    return jsonify({'data_received': True}), 200


@book_api.route('/book_recommendation', methods=['GET'])
def get_recommended_book():
    if request.headers.get('X-Mocking') == 'Enabled':
        log.info('serving mock',
                 extra={'endpoint': '/book_recommendation', 'method': request.method, 'request': str(request.json)})
        return jsonify(mock_recommendation), 200

    res = jsonify(recommendation.on_recommendation_requested(request))

    log.info('serving endpoint',
             extra={'endpoint': '/book_recommendation', 'method': request.method, 'request': str(request.json),
                    'response': res})
    return res, 200
