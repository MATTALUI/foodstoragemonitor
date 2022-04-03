import json
from sqlalchemy.orm import relationship
from .item_set_category import ItemSetCategory
from .category import Category

from .db import db

class ItemSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = relationship("Product", back_populates="item_sets")
    expiration = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    categories = db.relationship('Category', secondary=ItemSetCategory, lazy='subquery', backref=db.backref('item_sets', lazy=True))

    @property
    def product_name(self):
        return self.product.name

    @property
    def is_ignorable(self):
        for cat in self.categories:
            if cat.name == Category.IGNORABLE_EXPIRY_NAME:
                return True
        return False

    @property
    def is_drinkable(self):
        for cat in self.categories:
            if cat.name == Category.DRINKABLE_NAME:
                return True
        return False

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "product_name" : self.product_name,
            "expiration" : self.expiration.strftime("%Y-%m-%d"),
            "quantity" : self.quantity,
            "description" : self.description,
        })
