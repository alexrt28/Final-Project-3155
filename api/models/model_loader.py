from . import customer, orders, order_item, menu_item, review, payment, promo_code, ingredient, recipes

from ..dependencies.database import engine, Base

# added Base import above to eliminate all the lines of code below

def index():
    Base.metadata.create_all(engine)

    # orders.Base.metadata.create_all(engine)
    # customer.Base.metadata.create_all(engine)
    # order_item.Base.metadata.create_all(engine)
    # menu_item.Base.metadata.create_all(engine)
    # review.Base.metadata.create_all(engine)
    # payment.Base.metadata.create_all(engine)
    # promo_code.Base.metadata.create_all(engine)
    # ingredient.Base.metadata.create_all(engine)
    # recipes.Base.metadata.create_all(engine)