from . import orders, order_details, menu_items, recipes, ingredients, customers, promo_code, payment, reviews


def load_routes(app):
    app.include_router(customers.router)
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu_items.router)
    app.include_router(recipes.router)
    app.include_router(ingredients.router)
    app.include_router(promo_code.router)
    app.include_router(payment.router)
    app.include_router(reviews.router)
