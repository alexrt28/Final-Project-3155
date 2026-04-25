from . import customer, orders, order_item, menu_item, review, payment, promo_code, ingredients, recipes

from ..dependencies.database import engine, Base

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