from typing import List
from fastapi import FastAPI
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from models import Category, Product, Inventory, Sale
from fastapi import HTTPException
from schemas import (
    CategoryCreate, CategoryRead, ProductCreate, ProductRead,
    InventoryCreate, InventoryRead, SaleCreate, SaleRead
)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/categories/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter_by(is_deleted=False).all()


@app.get("/categories/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category or category.is_deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    db_inventory = Inventory(product_id=db_product.id, quantity=1)
    db.add(db_inventory)
    db.commit()

    return db_product


@app.get("/products/", response_model=List[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).filter_by(is_deleted=False).all()


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product or product.is_deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product or product.is_deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_deleted = True
    db.commit()
    return {"message": "Product soft-deleted"}


@app.post("/inventory/", response_model=InventoryRead)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


@app.get("/inventory/", response_model=List[InventoryRead])
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).filter_by(is_deleted=False).all()


@app.get("/inventory/{inventory_id}", response_model=InventoryRead)
def get_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).get(inventory_id)
    if not inventory or inventory.is_deleted:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inventory


@app.post("/sales/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@app.get("/sales/", response_model=List[SaleRead])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).filter_by(is_deleted=False).all()


@app.get("/sales/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).get(sale_id)
    if not sale or sale.is_deleted:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
