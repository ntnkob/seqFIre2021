import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-da-secret-key'
    OUTPUT_PATH = basedir = os.path.join(os.path.join(os.path.realpath(os.path.dirname(__file__)),'app'),'download')
