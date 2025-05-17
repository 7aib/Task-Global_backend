import os
import sys
import random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Category, Product, Inventory, Sale
from enums import SalesChannel

DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_demo_data():
    db: Session = SessionLocal()
    try:
        db.query(Sale).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.query(Category).delete()

        categories = [
            Category(name="Electronics", description="Gadgets and devices"),
            Category(name="Home Appliances", description="Kitchen and home utilities"),
            Category(name="Books", description="Fiction, non-fiction, educational"),
        ]
        db.add_all(categories)
        db.commit()

        products = [
            Product(name="Smartphone", price=699.99, description="Latest model", category=categories[0]),
            Product(name="Microwave", price=149.99, description="800W microwave", category=categories[1]),
            Product(name="Python Book", price=39.99, description="Learn Python", category=categories[2]),
        ]
        db.add_all(products)
        db.commit()

        for product in products:
            db.add(Inventory(product=product, stock=random.randint(10, 100)))
        db.commit()

        for product in products:
            for i in range(10):
                qty = random.randint(1, 5)
                db.add(Sale(
                    product=product,
                    quantity=qty,
                    total_price=qty * product.price,
                    sale_date=datetime.utcnow() - timedelta(days=random.randint(0, 90)),
                    channel=random.choice(list(SalesChannel)),
                    customer_email=f"user{i}@example.com",
                ))
        db.commit()

        print("✅ Demo data created successfully.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()
