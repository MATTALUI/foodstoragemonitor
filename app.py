from flask import Flask
import os

import blueprints
import config
from models import db

cwd = os.getcwd()
app = Flask(__name__)
db_path = "sqlite:///" + cwd + "/" + config.DATABASE_NAME + ".db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_path

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(blueprints.root_blueprint)       # Root routes and misc housekeeping
app.register_blueprint(blueprints.itemsets_blueprint)   # "/storage-items" routes
app.register_blueprint(blueprints.categories_blueprint) # "/categories" routes
app.register_blueprint(blueprints.products_blueprint)   # "/products" routes
app.register_blueprint(blueprints.groups_blueprint)     # "/groups" routes
app.register_blueprint(blueprints.cron_blueprint)       # "/cron" routes
