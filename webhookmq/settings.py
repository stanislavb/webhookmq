import os

DEBUG_ENV = os.getenv('DEBUG', 'False')
DEBUG = True if DEBUG_ENV == 'True' else False
ROOT_URLCONF = 'webhookmq.urls'
SECRET_KEY = os.getenv('SECRET_KEY')
MQ_URI = os.getenv('MQ_URI')
PATH_PREFIX = os.getenv('PATH_PREFIX')
