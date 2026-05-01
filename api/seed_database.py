from api.dependencies.database import SessionLocal
from api.models import customer, ingredients, menu_item, model_loader, orders, order_item, payment, promo_code, recipes, review
from datetime import datetime, timedelta

# == To populate your database for the first time ==
#
# In first terminal run: uvicorn api.main:app --reload
#
# Open 2nd terminal and run: python -m api.seed_database

def seed_all():
    db = SessionLocal()

    try:
        print("Creating Independent Tables: Customers, Menu Items, Ingredients and Promo Codes")

        new_customer1 = customer.Customer(
            name="Alex Roy",
            email="aroy27@charlotte.edu",
            phone="704-555-0197"
        )
        new_customer2 = customer.Customer(
            name="Elena Song",
            email="esong7@charlotte.edu",
            phone="704-555-0198"
        )
        new_customer3 = customer.Customer(
            name="Jasmine McCray",
            email="jmccray7@charlotte.edu",
            phone="704-555-0199"
        )
        new_customer4 = customer.Customer(
            name="Julian Dominguez",
            email="jdomin14@charlotte.edu",
            phone="704-555-0196"
        )

        turkey_club = menu_item.MenuItem(
            name="Turkey Club",
            price=12.99,
            category= "sandwich",
            calories=450
        )
        chicken_soup = menu_item.MenuItem(
            name="Chicken Soup",
            price=7.99,
            category="soup",
            calories=300
        )
        spaghetti = menu_item.MenuItem(
            name="Spaghetti",
            price=14.99,
            category="pasta",
            calories=900
        )

        bread = ingredients.Ingredient(
            name="bread",
            quantity=12,
            unit="slice"
        )
        turkey = ingredients.Ingredient(
            name="turkey",
            quantity=10,
            unit="slice"
        )
        broth = ingredients.Ingredient(
            name="broth",
            quantity=40,
            unit="oz"
        )
        ground_chicken = ingredients.Ingredient(
            name="ground_chicken",
            quantity=24,
            unit="oz"
        )
        linguine = ingredients.Ingredient(
            name="linguine",
            quantity=12,
            unit="serving"
        )
        marinara = ingredients.Ingredient(
            name="marinara",
            quantity=8,
            unit="cup"
        )

        yesterday = datetime.now() - timedelta(days=1)
        three_days_ago = datetime.now() - timedelta(days=3)

        percent_off_20 = promo_code.PromoCode(
            promo_code="TAKE20",
            discount=20,
            discount_type="% off",
            expiry=yesterday
        )
        percent_off_30 = promo_code.PromoCode(
            promo_code="TAKE30",
            discount=30,
            discount_type="% off",
            expiry=three_days_ago
        )

        db.add_all([new_customer1, new_customer2, new_customer3, new_customer4,
                    turkey_club, chicken_soup, spaghetti,
                    bread, turkey, broth, ground_chicken, linguine, marinara,
                    percent_off_20, percent_off_30])
        db.commit()

        print("Creating First Children Tables: Orders, Recipes")

        order_1 = orders.Order(
            customer_id=new_customer1.id,
            promo_code_id=percent_off_30.id,
            order_date=three_days_ago,
            order_type="takeout",
            tracking_number="TRACKING-001",
            status = "completed",
            total_price = 12.99
        )
        order_6 = orders.Order(
            customer_id=new_customer3.id,
            promo_code_id=percent_off_20.id,
            order_date=yesterday,
            order_type="delivery",
            tracking_number="TRACKING-004",
            status="completed",
            total_price=22.98
        )

        recipe_turkey_1 = recipes.Recipe(
            menu_item_id=turkey_club.id,
            ingredient_id=bread.id,
            quantity=2
        )
        recipe_turkey_2 = recipes.Recipe(
            menu_item_id=turkey_club.id,
            ingredient_id=turkey.id,
            quantity=4
        )

        recipe_spaghetti_1 = recipes.Recipe(
            menu_item_id=spaghetti.id,
            ingredient_id=linguine.id,
            quantity=2
        )

        recipe_spaghetti_2 = recipes.Recipe(
            menu_item_id=spaghetti.id,
            ingredient_id=marinara.id,
            quantity=1
        )


        db.add_all([order_1, order_6, recipe_turkey_1, recipe_turkey_2, recipe_spaghetti_1, recipe_spaghetti_2])
        db.commit()

        print("Creating Second Children Tables: Order_Item, Payment, Review")

        order_1_item_1 = order_item.OrderItem(
            order_id=order_1.id,
            menu_item_id=turkey_club.id,
            quantity=1,
            subtotal=12.99
        )
        order_6_item_1 = order_item.OrderItem(
            order_id=order_6.id,
            menu_item_id=spaghetti.id,
            quantity=1,
            subtotal=14.99
        )
        order_6_item_2 = order_item.OrderItem(
            order_id=order_6.id,
            menu_item_id=chicken_soup.id,
            quantity=1,
            subtotal=7.99
        )

        payment_1 = payment.Payment(
            order_id=order_1.id,
            payment_type="credit card",
            card_info="**** **** **** 1234",
            status="completed"
        )
        payment_6 = payment.Payment(
            order_id=order_6.id,
            payment_type="cash",
            card_info="None",
            status="completed"
        )

        review_1 = review.Review(
            menu_item_id=turkey_club.id,
            customer_id=new_customer1.id,
            rating=5,
            comment="The best turkey club in Charlotte, I loved it!"
        )
        review_2 = review.Review(
            menu_item_id=spaghetti.id,
            customer_id=new_customer3.id,
            rating=3,
            comment="Meh"
        )

        db.add_all([order_1_item_1, order_6_item_1, order_6_item_2, payment_1, payment_6, review_1, review_2])
        db.commit()

        print("Database Seeded!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()