from flask import Blueprint, redirect, send_from_directory

root_blueprint = Blueprint('root_blueprint', __name__)

@root_blueprint.route('/')
def root():
    return redirect("/storage-items")

@root_blueprint.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('static/assets', path)
