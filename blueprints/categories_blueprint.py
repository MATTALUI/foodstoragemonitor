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

@categories_blueprint.route("/categories/new/")
def new_category():
    return render_template('categories/form.html')


def index():
    # TODO: we can change sorts  here
    search = request.args.get("search") or None
    categories = categories = Category.query
    if search is not None:
        categories = categories.filter(func.lower(Category.name).contains(search.lower()))
    categories = categories.all()
    return render_template(
        'categories/index.html',
        params=request.args,
        categories=categories,
    )

def create():
    data = json.loads(request.data)
    cat = Category(**data)
    db.session.add(cat)
    db.session.commit()
    return 'true'
