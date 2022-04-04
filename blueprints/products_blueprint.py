from flask import Blueprint, request, render_template, redirect
import json
import requests
from sqlalchemy import func
from bs4 import BeautifulSoup
from models import db, Product, ItemSet

products_blueprint = Blueprint('products_blueprint', __name__)

###############################################################################
# PRODUCTS ROUTES
###############################################################################
@products_blueprint.route("/products.json/", methods=['GET'])
def get_products_list():
    upc = request.args.get("upc") or None
    if request.method == 'GET' and upc is not None:
        return query_upc()
    elif request.method == 'GET':
        return products_list()

@products_blueprint.route("/products/", methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        return index()
    elif request.method == 'POST':
        return create()

@products_blueprint.route("/products/<product_id>/", methods=['GET', 'POST', 'DELETE'])
def item_set(product_id):
    if request.method == 'GET':
        return product_id
    elif request.method == 'POST':
        return update(product_id)
    elif request.method == 'DELETE':
        return destroy(product_id)

@products_blueprint.route("/products/<product_id>/edit/", methods=['GET'])
def edit_product(product_id):
    return edit(product_id)

def index():
    # TODO: We can change sorting here.
    search = request.args.get("search") or None
    products = Product.query
    if search is not None:
        products = products.filter(func.lower(Product.name).contains(search.lower()))

    products = products.order_by(func.lower(Product.name).asc()).all()
    return render_template(
        'products/index.html',
        params=request.args,
        products=products
    )

def edit(product_id):
    product = Product.query.get(product_id)
    return render_template(
        'products/form.html',
        product=product
    )

def create():
    # Because we really only create products
    # through the itemset form at this point
    pass

def update(product_id):
    product = Product.query.get(product_id)
    product.name = request.form.get('name')
    db.session.add(product)
    db.session.commit()
    return redirect('/products')

def destroy(product_id):
    items = ItemSet.query.filter(ItemSet.product_id == product_id).delete()
    product = Product.query.get(product_id)
    db.session.delete(product)
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

def query_upc():
    try:
        # This UPC should always have a value, because we don't hit the route if not
        upc = request.args.get("upc")
        # First, we check to see if we already have the product saved
        product = Product.get_by_upc(upc)
        size = None
        if product is None:
            # If we don't already have it, we need to scrape it from the UPC database
            url = f"https://www.upcdatabase.com/item/{upc}"
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')
            name = soup.find_all('td')[8].text
            size = soup.find_all('td')[11].text
            product = Product(name=name)

        return json.dumps({
            "product": {
                "id": product.id or None,
                "name": product.name,
                "upc_code": upc
            },
            "is_new": product.id is None,
            "size": size,
        })
    except:
        return json.dumps({
            "error": "Unable to locate UPC data."
        })
