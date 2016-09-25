from flask import Flask

from api import config
from api.books_recommendation_api import book_api
from api.errors.error_handler import error_handler_api
from utils import logger

app = Flask(__name__)
app.register_blueprint(book_api)
app.register_blueprint(error_handler_api)
log = logger.define_logger('API started')

if __name__ == '__main__':
    log.info('service ready', extra={'server': {'host': config.HOST, 'port': config.PORT}})
    app.run(debug=True, host=config.HOST, port=config.PORT)
