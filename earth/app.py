from flask import Flask, request, render_template
from flask.json import jsonify
from glob import glob
from .validate_yaml import get_yaml
import os
app = Flask(__name__)


def create_db(yaml_filelist):
    db = []
    for x in yaml_files:
        entry = get_yaml(x)
        entry["id"] = x
        entry["basename"] = os.path.basename(x)[:-4]
        db.append(entry)
    return db


catalog_location = os.environ.get("CATALOG_FOLDER", os.path.curdir)
yaml_files = glob(os.path.join(catalog_location, "*.yml"))
db = create_db(yaml_files)


def filter_by_keywords(db, request):
    return db


def filter_by_detailed_search(db, request):
    return db


def _uniques(key):
    result = set()
    for x in db:
        result = set(list(result) + x[key])
    return result


@app.route('/')
def hello_world():
    return render_template("index.html", db=db)


@app.route('/search')
def search():
    results = filter_by_keywords(db, request.args)
    return render_template("search.html", **request.args, results=results)


@app.route('/detailedsearch')
def detailedsearch(rights=None):
    rights = _uniques('rights')  # Fix options
    results = filter_by_detailed_search(db, request.args)
    return render_template("detailedsearch.html", **request.args, rights=rights, results=results)


@app.route('/dataset/<dataset>')
def dataset(dataset):
    path = os.path.join(catalog_location, dataset+'.yml')
    meta = get_yaml(path)
    return jsonify(meta)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": 404, "message": "Page does not exist"})
