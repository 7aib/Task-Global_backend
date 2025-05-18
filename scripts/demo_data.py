import os
import sys
import random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Category, Product, Inventory, Sale, InventoryLog
from enums import SalesChannel, ChangeReason

DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_demo_data():
    db: Session = SessionLocal()
    try:
        # Soft-delete existing data
        db.query(Sale).filter_by(is_deleted=False).update({"is_deleted": True})
        db.query(InventoryLog).filter_by(is_deleted=False).update({"is_deleted": True})
        db.query(Inventory).filter_by(is_deleted=False).update({"is_deleted": True})
        db.query(Product).filter_by(is_deleted=False).update({"is_deleted": True})
        db.query(Category).filter_by(is_deleted=False).update({"is_deleted": True})
        db.commit()

        # Create categories
        categories = [
            Category(name="Electronics", description="Gadgets and devices"),
            Category(name="Home Appliances", description="Kitchen and home utilities"),
            Category(name="Books", description="Fiction, non-fiction, educational"),
        ]
        db.add_all(categories)
        db.commit()

        # Create products
        products = [
            Product(
                name="Smartphone",
                price=699.99,
                description="Latest model",
                category=categories[0],
            ),
            Product(
                name="Microwave",
                price=149.99,
                description="800W microwave",
                category=categories[1],
            ),
            Product(
                name="Python Book",
                price=39.99,
                description="Learn Python",
                category=categories[2],
            ),
        ]
        db.add_all(products)
        db.commit()

        # Create inventory
        inventories = []
        for product in products:
            inventory = Inventory(product=product, stock=random.randint(10, 100))
            db.add(inventory)
            inventories.append(inventory)
        db.commit()

        # Create inventory logs (simulate stock changes)
        for inventory in inventories:
            initial_stock = inventory.stock
            for i in range(3):  # Simulate 3 stock changes per inventory
                old_stock = inventory.stock
                stock_change = random.randint(-5, 10)  # Random change
                new_stock = max(0, old_stock + stock_change)  # Prevent negative stock

                # Determine change reason based on stock change
                if stock_change > 0:
                    reason = ChangeReason.RESTOCK
                elif stock_change < 0:
                    reason = random.choice(
                        [ChangeReason.SALE, ChangeReason.DAMAGE, ChangeReason.RETURN]
                    )
                else:
                    reason = ChangeReason.MANUAL_ADJUSTMENT

                inventory.stock = new_stock
                db.add(
                    InventoryLog(
                        inventory=inventory,
                        old_stock=old_stock,
                        new_stock=new_stock,
                        change_reason=reason,
                        change_date=datetime.utcnow()
                        - timedelta(days=random.randint(0, 90)),
                    )
                )
        db.commit()

        # Create sales
        for product in products:
            for i in range(10):
                qty = random.randint(1, 5)
                db.add(
                    Sale(
                        product=product,
                        quantity=qty,
                        total_price=qty * product.price,
                        sale_date=datetime.utcnow()
                        - timedelta(days=random.randint(0, 90)),
                        channel=random.choice(list(SalesChannel)),
                        customer_email=f"user{i}@example.com",
                    )
                )
        db.commit()

        print("✅ Demo data created successfully.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()
