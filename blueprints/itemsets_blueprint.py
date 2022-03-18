from flask import Blueprint, request, render_template
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import date, datetime
import json

from models import db, ItemSet, Category, Group, Product
from utils import get_warning_date, get_highlight_date

itemsets_blueprint = Blueprint('itemsets_blueprint', __name__)

###############################################################################
# STORAGE ITEM ROUTES
###############################################################################
@itemsets_blueprint.route("/storage-items", methods=['GET', 'POST'])
def storage_items():
    if request.method == 'GET':
        return index()
    elif request.method == 'POST':
        return create()

@itemsets_blueprint.route("/storage-items/<item_set_id>", methods=['DELETE'])
def item_set(item_set_id):
    if request.method == 'DELETE':
        return delete_item_set(item_set_id)

@itemsets_blueprint.route("/storage-items/new")
def new_item():
    return render_template('items/form.html')

@itemsets_blueprint.route("/storage-items/<item_set_id>/increment", methods=['POST'])
def increment_item_set(item_set_id):
    item_set = ItemSet.query.get(item_set_id)
    item_set.quantity += 1
    db.session.add(item_set)
    db.session.commit()
    return 'true'

@itemsets_blueprint.route("/storage-items/<item_set_id>/decrement", methods=['POST'])
def decrement_item_set(item_set_id):
    item_set = ItemSet.query.get(item_set_id)
    item_set.quantity -= 1
    db.session.add(item_set)
    db.session.commit()
    return 'true'

def index():
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

def get_item_set_context(item_set):
    # Check if already expired
    if item_set.expiration < date.today():
        return "danger"
    # Check if expiry in next 2 weeks
    if item_set.expiration < get_warning_date():
        return "warning"
    # Check if expiry in next month
    if item_set.expiration < get_highlight_date():
        return "info"
    return "default"

def create():
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

    return 'true'

def delete_item_set(item_set_id):
    item_set = ItemSet.query.get(item_set_id)
    db.session.delete(item_set)
    db.session.commit()
    return 'true'
