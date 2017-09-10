import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_ROOT = 'views/blog/content'
    POST_DIR = 'posts'
    SMTH = b'$2b$12$D9fukiXJ5Ik7LE1FpjgIB.xhZg1ln2pTCd/J3IVXAbun3dWSNxml6'
    USRNAME = b'$2b$12$mqF/WBETzPrANdYsueTO1u/jDIe.sVUyvq1fgTDEKccSWkvREqhB6'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    USRNAME = b'$2b$12$wAqg4uygGSKBmOc7FbkO..WlipF9xp9548i5leT8PcyF49An18G.i'
    SMTH = b'$2b$12$1RtOT/TPDqWXvMIFPvCkyu4K25/K3p4ZTtTkGGJLHavRYTR0ZO5qG'
