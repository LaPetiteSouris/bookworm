import uuid

from pymongo import MongoClient

from database import neo4j, config
from utils import logger, hmac_helper

log = logger.define_logger('User Authentication')
MONGO_URI = 'mongodb://{}:{}@ds048319.mlab.com:48319/bookworm'.format('api', 'pass')
SECRET_KEY = 'This is secret. Seriously !'

db = MongoClient(MONGO_URI)['bookworm']
graph_client = neo4j.SmartGraph(log=log, uri=config.URI)


def on_user_signup(request):
    username = request.args.get('username')
    password = request.args.get('password')

    user = db.users.find_one({'username': username})

    # Check if user exists
    if user:
        return None

    # create new user

    user_id = str(uuid.uuid4())
    hmac_pass = hmac_helper.make_hmac(SECRET_KEY.encode('UTF-8'), password.encode('UTF-8'))
    db.users.insert({'user_id': user_id, 'username': username, 'password': hmac_pass})
    log.info('new user created', extra={'user_id': user_id})

    # Todo: Create new user node in Graph DB
    graph_client.find_node(label='User', node_name=user_id)

    return user_id


def on_user_auth_request(request):
    username = request.args.get('username')
    password = request.args.get('password')
    user = db.users.find_one({'username': username})

    if not user:
        return False

    user_pwd_hash = user.get('password')
    pwd_in_request = hmac_helper.make_hmac(SECRET_KEY.encode('UTF-8'), password.encode('UTF-8'))

    # ToDo: Should user HMAC Verification to avoid unsafe hmac string comparison
    if user_pwd_hash == pwd_in_request:
        log.info('user authenticated', extra={'user_id': user.get('user_id')})
        return True

    log.info('user authenticated', extra={'user_in_request': username, 'password_in_request': password})
    return False
