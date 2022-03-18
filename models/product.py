from sqlalchemy.orm import relationship

from .db import db
from .product_category import ProductCategory
from .product_group import ProductGroup

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    item_sets = relationship("ItemSet",  back_populates="product")
    groups = db.relationship('Group', secondary=ProductGroup, lazy='subquery', backref=db.backref('products', lazy=True))
    categories = db.relationship('Category', secondary=ProductCategory, lazy='subquery', backref=db.backref('products', lazy=True))

    @property
    def total_items(self):
        return sum(item_set.quantity for item_set in self.item_sets)
