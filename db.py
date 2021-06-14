import os
from flask_sqlalchemy import SQLAlchemy


def load_database_url():
    url = 'sqlite:///data.db'
    if os.environ.get('DATABASE_URL'):
        url = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    elif os.environ.get('DATABASE_HOST'):
        host, port, user, password, dbname = (
            os.environ['DATABASE_HOST'],
            os.environ['DATABASE_PORT'],
            os.environ['DATABASE_USER'],
            os.environ['DATABASE_PASSWORD'],
            os.environ['DATABASE_NAME'],
        )
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return url


db = SQLAlchemy()
