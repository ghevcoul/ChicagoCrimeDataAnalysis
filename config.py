import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://localhost/crimes"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Socrata Info
APP_TOKEN = None