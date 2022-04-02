from .db import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    bg_hex = db.Column(db.String(256), nullable=False, default='#000000')
    text_hex = db.Column(db.String(256), nullable=False, default='#FFFFFF')

    IGNORABLE_EXPIRY_NAME = 'Ignorable Expiry'

    @classmethod
    def get_ignorable_expiry(cls):
        return cls.query.filter(cls.name==cls.IGNORABLE_EXPIRY_NAME).first()

    def to_chip_ele(self):
        return f"<span class=\"badge\" style=\"background-color: {self.bg_hex}; color: {self.text_hex}\">{self.name}</span>"
