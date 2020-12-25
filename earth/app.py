from flask import Flask, request, render_template
from flask.json import jsonify
from glob import glob
from .validate_yaml import get_yaml
import os
app = Flask(__name__)

# Initiate database
catalog_location = os.environ.get("CATALOG_FOLDER", os.path.curdir)
yaml_files = glob(os.path.join(catalog_location, "*.yml"))
db = []
for x in yaml_files:
    entry = get_yaml(x)
    entry["id"] = x
    db.append(entry)


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
    req = request.args
    return render_template("search.html")


@app.route('/detailedsearch')
def detailedsearch(rights=None):
    rights = _uniques('rights')
    return render_template("detailedsearch.html", rights=rights)


@app.route('/dataset/<dataset>')
def dataset(dataset):
    path = os.path.join(catalog_location, dataset+'.yml')
    meta = get_yaml(path)
    return jsonify(meta)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": 404, "message": "Page does not exist"})
