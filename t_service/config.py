import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
        'user': 'tester',
        'pw': 'W4terl001',
        'db': 'file_changesdb',
        'host': 'huidocker',
        'port': '5432',
}

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
    #                           %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_DATABASE_URI = 'postgresql://tester:W4terl001@MotionTesting:5432/file_changesdb'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
