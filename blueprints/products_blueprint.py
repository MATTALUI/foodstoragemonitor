from flask import Blueprint, request
import json
from sqlalchemy import func
from models import Product

products_blueprint = Blueprint('products_blueprint', __name__)

###############################################################################
# PRODUCTS ROUTES
###############################################################################
@products_blueprint.route("/products.json", methods=['GET'])
def get_products_list():
    if request.method == 'GET':
        return products_list()

def products_list():
    search = request.args.get("term") or None
    products = Product.query
    if search is not None:
        products = products.filter(func.lower(Product.name).contains(search.lower()))
    products = products.limit(10).all()
    product_names = [product.name for product in products]
    return json.dumps(product_names)
