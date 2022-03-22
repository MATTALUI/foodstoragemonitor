from flask import Blueprint, request, render_template
import json
from sqlalchemy import func
from models import db, Category

categories_blueprint = Blueprint('categories_blueprint', __name__)

###############################################################################
# CATEGORY ROUTES
###############################################################################
@categories_blueprint.route("/categories/", methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        return index()
    elif request.method == 'POST':
        return create()

@categories_blueprint.route("/categories/<category_id>/", methods=['POST', 'DELETE'])
def category(category_id):
    if request.method == 'POST':
        return update(category_id)
    elif request.method == 'DELETE':
        return destroy(category_id)

@categories_blueprint.route("/categories/new/")
def new_category():
    return new()

@categories_blueprint.route("/categories/<category_id>/edit/")
def edit_category(category_id):
    return edit(category_id)


def index():
    # TODO: we can change sorts  here
    search = request.args.get("search") or None
    categories = categories = Category.query
    if search is not None:
        categories = categories.filter(func.lower(Category.name).contains(search.lower()))
    categories = categories.order_by(func.lower(Category.name).asc()).all()
    return render_template(
        'categories/index.html',
        params=request.args,
        categories=categories,
    )

def new():
    return render_template('categories/form.html')

def edit(category_id):
    category = Category.query.get(category_id)
    print(category)
    print(category.name)
    return render_template('categories/form.html', category=category)

def create():
    return upsert_category()

def update(category_id):
    return upsert_category()

def upsert_category():
    data = json.loads(request.data)
    # cat = Category(**data)
    cat = Category()
    if 'id' in data:
        cat = Category.query.get(data['id'])
    cat.name = data['name']
    db.session.add(cat)
    db.session.commit()
    return 'true'

def destroy(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return 'true'
