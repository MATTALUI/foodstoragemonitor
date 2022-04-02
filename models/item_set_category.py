from .db import db

ItemSetCategory = db.Table('item_set_category',
    db.Column('item_set_id', db.Integer, db.ForeignKey('item_set.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)
