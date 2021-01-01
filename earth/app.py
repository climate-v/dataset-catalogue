import os
import json
from glob import glob

from flask import Flask, request, render_template
from flask.json import jsonify

from .validate_yaml import get_yaml
from .base import app, db, _get_db_uri

def initdb():
    db.drop_all()
    db.create_all()
    _load_datasets_into(db)
    raw_sql('CREATE EXTENSION IF NOT EXISTS fuzzystrmatch')
    raw_sql('CREATE EXTENSION IF NOT EXISTS pg_trgm')

def main():
    app.run(host=os.environ.get('FLASK_RUN_HOST'),
            port=os.environ.get('FLASK_RUN_PORT'))


##############
### Models ###
##############

class Dataset(db.Model):
    id = db.Column(db.String, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        result = self.data.copy()
        result['id'] = self.id
        return json.dumps(result)


################
### Database ###
################


def _load_datasets_into(db):
    catalog_location = os.environ.get("CATALOG_FOLDER", os.path.curdir)
    yaml_files = glob(os.path.join(catalog_location, "*.yml"))
    for x in yaml_files:
        entry = get_yaml(x)
        entry = Dataset(id=os.path.basename(x)[:-4], data=entry)
        db.session.add(entry)
        db.session.commit()

# TODO: Currently inefficient due to engine creation at every call
# TODO: Run commands via SQLAlchemy via JSONB https://stackoverflow.com/questions/29974143/python-sqlalchemy-and-postgres-how-to-query-a-json-element
def raw_sql(cmd):
    """ Execute raw SQL command on the database
    """
    from sqlalchemy import create_engine
    db_uri = _get_db_uri()
    engine = create_engine(db_uri)
    with engine.connect() as con:
        result = con.execute(cmd)
    return result

##############
### Routes ###
##############


@app.route('/')
def hello_world():
    results = Dataset.query.all()
    return render_template("index.html", db=results)


@app.route('/search')
def search():
    results = Dataset.query.all()
    return render_template("search.html", **request.args, results=results)


@app.route('/detailedsearch')
def detailedsearch(rights=None):
    results = raw_sql('SELECT * FROM dataset')
    return render_template("detailedsearch.html", **request.args, results=results)


@app.route('/dataset/<dataset>')
def dataset(dataset):
    dataset = Dataset.query.filter_by(id=dataset).first_or_404()
    return jsonify(dataset.data)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": 404, "message": "Page does not exist"})
