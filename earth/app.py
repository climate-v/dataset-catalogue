from flask import Flask, request
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

@app.route('/')
def hello_world():
    return jsonify(db)


@app.route('/search')
def search():
    return jsonify(request.args)


@app.route('/detailedsearch')
def detailedsearch():
    return jsonify(request.args)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": 404, "message": "Page does not exist"})
