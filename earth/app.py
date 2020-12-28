import os
import json
from glob import glob

from flask import Flask, request, render_template
from flask.json import jsonify

from .validate_yaml import get_yaml
from .base import app, db, _get_db_uri

def main():
    db.drop_all()
    db.create_all()
    _load_datasets_into(db)

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
    results = Dataset.query.all()
    return render_template("detailedsearch.html", **request.args, results=results)


@app.route('/dataset/<dataset>')
def dataset(dataset):
    dataset = Dataset.query.filter_by(id=dataset).first_or_404()
    return jsonify(dataset.data)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": 404, "message": "Page does not exist"})
