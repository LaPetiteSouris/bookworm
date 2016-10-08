import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask

from api import config
from api.routes import book_api
from api.errors.error_handler import error_handler_api
from pawns import book_hunter, distance_calculator
from utils import logger

log = logger.define_logger('API started')

app = Flask(__name__)
app.register_blueprint(book_api)
app.register_blueprint(error_handler_api)
#
# # Setup cron
# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(
#     func=book_hunter.launch,
#     trigger=IntervalTrigger(hours=24),
#     id='book_hunter',
#     name='Hunt for book from Google  Book API',
#     replace_existing=False)
#
# scheduler.add_job(
#     func=distance_calculator.launch,
#     trigger=IntervalTrigger(hours=24),
#     id='distance_calculator',
#     name='Calculate distance between users',
#     replace_existing=False)
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    log.info('service ready', extra={'server': {'host': config.HOST, 'port': config.PORT}})
    app.run(debug=False, host=config.HOST, port=config.PORT)
