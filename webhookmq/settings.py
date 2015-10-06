import os

DEBUG_ENV = os.getenv('DEBUG', 'False')
if DEBUG_ENV == 'True':
    DEBUG = True
else:
    DEBUG = False

ROOT_URLCONF = 'webhookmq.urls'
SECRET_KEY = os.getenv('SECRET_KEY')
MQ_URI = os.getenv('MQ_URI', 'amqp://guest:guest@rabbitmq//')
PATH_PREFIX = os.getenv('PATH_PREFIX')
