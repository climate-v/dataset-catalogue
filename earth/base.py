import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def _get_environ(key):
    result = os.environ.get(key, None)
    if result is None:
        raise Exception(f"Expected environment variable '{key}' to be set.")
    return result

def _get_db_uri():
    user = _get_environ('POSTGRES_USER')
    pw = _get_environ('POSTGRES_PASSWORD')
    url = _get_environ('POSTGRES_URL')
    database = _get_environ('POSTGRES_DB')
    db_url = f'postgresql+psycopg2://{user}:{pw}@{url}/{database}'
    return db_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = _get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
