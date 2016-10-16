""" gunicorn wsgi server configuration. """

from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count() * 2


bind = '0.0.0.0:' + environ.get('PORT', '8000')
max_requests = environ.get('GUNICORN_MAX_REQUESTS', 1000)
worker_class = 'gevent'
workers = environ.get('GUNICORN_WORKERS', max_workers())
