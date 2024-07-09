from celery import Celery
from project import app
from project.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    'project',
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
    include=['project.tasks'],
)
celery.conf.update(app.config)
celery.conf.broker_connection_retry_on_startup = True
celery.conf.broker_transport_options = {'visibility_timeout': 3600}
