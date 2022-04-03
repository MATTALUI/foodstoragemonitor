from .db import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    bg_hex = db.Column(db.String(256), nullable=False, default='#000000')
    text_hex = db.Column(db.String(256), nullable=False, default='#FFFFFF')

    IGNORABLE_EXPIRY_NAME = 'Ignorable Expiry'
    DRINKABLE_NAME = 'Drinkable'

    @classmethod
    def get_ignorable_expiry(cls):
        return cls.query.filter(cls.name==cls.IGNORABLE_EXPIRY_NAME).first()

    @classmethod
    def get_drinkable(cls):
        return cls.query.filter(cls.name==cls.DRINKABLE_NAME).first()

    def to_chip_ele(self):
        return f"<span class=\"badge category\" style=\"background-color: {self.bg_hex}; color: {self.text_hex}\" data-category=\"{self.id}\">{self.name}</span>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bg_hex": self.bg_hex,
            "text_hex": self.text_hex
        }
