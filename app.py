import sqlite3
from flask import Flask, g, redirect, request, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import func
from datetime import datetime, date, timedelta
import os
import json

cwd = os.getcwd()
# env = Environment(extensions=[HamlishExtension])
app = Flask(__name__)
db_path = "sqlite:///" + cwd + "/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy(app)


ProductGroup = db.Table('product_group',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

ProductCategory = db.Table('product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    item_sets = relationship("ItemSet",  back_populates="product")
    groups = db.relationship('Group', secondary=ProductGroup, lazy='subquery', backref=db.backref('products', lazy=True))
    categories = db.relationship('Category', secondary=ProductCategory, lazy='subquery', backref=db.backref('products', lazy=True))

class ItemSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = relationship("Product", back_populates="item_sets")
    expiration = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    @property
    def product_name(self):
        return self.product.name

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

db.create_all()

def get_item_set_context(item_set):
    today = date.today()
    # Check if already expired
    if item_set.expiration < today:
        return "danger"
    # Check if expiry in next 2 weeks
    if item_set.expiration < today + timedelta(weeks=2):
        return "warning"
    # Check if expiry in next month
    if item_set.expiration < today + timedelta(weeks=4):
        return "info"
    return "default"

def build_product_name_items_table(item_sets, order="asc"):
    table_items = {}
    # Build base item table
    for item_set in item_sets:
        if item_set.product_id not in table_items:
            table_items[item_set.product_id] = {
                "product_name": item_set.product_name,
                "product_id": item_set.product_id,
                "item_sets": []
            }
        print(type(item_set.expiration))
        table_items[item_set.product_id]["item_sets"].append({
            "data": item_set,
            "context": get_item_set_context(item_set)
        })

    # Order item sets by date
    linear_table = []
    for product_id in table_items:
        product_data = table_items[product_id]
        product_data['item_sets'].sort(key=lambda d: d["data"].expiration)
        linear_table.append(product_data)

    # Convert to array and order by product_name
    linear_table.sort(key=lambda d: d['product_name'].lower(), reverse=order=="desc")
    print(linear_table)

    return linear_table


def item_set_index():
    # Extract Search Params
    search = request.args.get("search") or None

    item_sets = ItemSet.query
    if search is not None:
        item_sets = item_sets.join(Product).filter(func.lower(Product.name).contains(search.lower()))
    item_sets = item_sets.options(joinedload(ItemSet.product)).all()
    # TODO: we can change sorts  here
    items_table = build_product_name_items_table(item_sets)
    categories = Category.query.all()
    groups = Group.query.all()
    return render_template(
        'items/index.html',
        items_table=items_table,
        params=request.args,
        item_sets=item_sets,
        categories=categories,
        groups=groups,
    )

def create_storage_item():
    # print(json.loads(request.data))
    for item_set_data in json.loads(request.data):

        product_name = item_set_data['product_name']
        product = Product.query.filter(func.lower(Product.name)==product_name.lower()).first()
        if product is None:
            product = Product(name=product_name)
            db.session.add(product)
            db.session.commit()
        db.session.add(ItemSet(
            product_id=product.id,
            description=item_set_data['description'],
            quantity=item_set_data['quantity'],
            expiration=datetime.strptime(item_set_data['expiration'], '%Y-%m-%d'),
        ))

    db.session.commit()

    # date = datetime.strptime(a, '%Y%m%d').strftime('%m/%d/%Y')
    return 'true'

def delete_item_set(item_set_id):
    item_set = ItemSet.query.get(item_set_id)
    db.session.delete(item_set)
    db.session.commit()
    return 'true'


def categories_index():
    # item_sets = ItemSet.query
    # item_sets = item_sets.options(joinedload(ItemSet.product)).all()
    # TODO: we can change sorts  here
    # items_table = build_product_name_items_table(item_sets)
    categories = Category.query.all()
    # groups = Group.query.all()
    return render_template(
        'categories/index.html',
        # items_table=items_table,
        params=request.args,
        # item_sets=item_sets,
        categories=categories,
        # groups=groups,
    )

def create_category():
    data = json.loads(request.data)
    cat = Category(**data)
    db.session.add(cat)
    db.session.commit()
    return 'true'

def products_list():
    search = request.args.get("term") or None
    products = Product.query
    if search is not None:
        products = products.filter(func.lower(Product.name).contains(search.lower()))
    products = products.limit(10).all()
    product_names = [product.name for product in products]
    return json.dumps(product_names)

###############################################################################
# BASE ROUTES
###############################################################################
@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static/assets', path)

@app.route("/")
def root():
    return redirect("/storage-items")


###############################################################################
# STORAGE ITEM ROUTES
###############################################################################
@app.route("/storage-items", methods=['GET', 'POST'])
def storage_items():
    if request.method == 'GET':
        return item_set_index()
    elif request.method == 'POST':
        return create_storage_item()

@app.route("/storage-items/<item_set_id>", methods=['DELETE'])
def item_set(item_set_id):
    if request.method == 'DELETE':
        return delete_item_set(item_set_id)

@app.route("/storage-items/new")
def new_item():
    return render_template('items/form.html')

@app.route("/storage-items/<item_set_id>/increment", methods=['POST'])
def increment_item_set(item_set_id):
    item_set = ItemSet.query.get(item_set_id)
    item_set.quantity += 1
    db.session.add(item_set)
    db.session.commit()
    return 'true'

@app.route("/storage-items/<item_set_id>/decrement", methods=['POST'])
def decrement_item_set(item_set_id):
    item_set = ItemSet.query.get(item_set_id)
    item_set.quantity -= 1
    db.session.add(item_set)
    db.session.commit()
    return 'true'


###############################################################################
# CATEGORY ROUTES
###############################################################################
@app.route("/categories", methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        return categories_index()
    elif request.method == 'POST':
        return create_category()

@app.route("/categories/new")
def new_category():
    return render_template('categories/form.html')


###############################################################################
# GROUP ROUTES
###############################################################################

###############################################################################
# PRODUCTS ROUTES
###############################################################################
@app.route("/products-list", methods=['GET'])
def get_products_list():
    if request.method == 'GET':
        return products_list()
