from flask import Blueprint, redirect, send_from_directory, send_file

root_blueprint = Blueprint('root_blueprint', __name__)

@root_blueprint.route('/')
def root():
    return redirect("/storage-items")

@root_blueprint.route('/assets/<path:path>/')
def send_asset(path):
    return send_from_directory('static/assets', path)

@root_blueprint.route('/manifest.json', methods=['GET'])
def send_manifest():
    return send_file('static/manifest.json')

@root_blueprint.route('/service-worker.js', methods=['GET'])
def send_service_worker():
    return send_file('static/service-worker.js')