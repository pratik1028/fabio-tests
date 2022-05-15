from celery import Celery
from flask import Flask


flask_app = Flask(__name__)
celery_app = Celery(flask_app.name,
                    include=['wikipedia.continent',
                             'wikipedia.country',
                             'wikipedia.city']
                    )
# celery_app.conf.broker_url = "amqp://myuser:mypassword@localhost/myvhost"
celery_app.conf.broker_url = "amqp://myuser:mypassword@localhost:5672/myvhost"
celery_app.conf.result_backend = 'db+sqlite:///results.sqlite'

import wikipedia.views


