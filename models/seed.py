from .db import db
from .category import Category

def run_seeds():
    seed_messages = []

    # Create a category for itemsets where we can ignore the expiry
    ignorable_expiry = Category.get_ignorable_expiry()
    if ignorable_expiry is None:
        ignorable_expiry = Category(
            name=Category.IGNORABLE_EXPIRY_NAME,
            bg_hex="#ac011d",
            text_hex="#FEFEFE"
        )
        db.session.add(ignorable_expiry)
        db.session.commit()
        seed_messages.append(f"Created category: {ignorable_expiry.name}")

    if len(seed_messages) > 0:
        print("===========RUNNING SEEDS===========")
        for message in seed_messages:
            print(message)
        print("===================================")
