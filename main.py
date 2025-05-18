from typing import List
from fastapi import FastAPI
from sqlalchemy import func
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, status
from datetime import datetime, timedelta

from enums import (
    ChangeReason,
    InventoryStatus,
    Quantity,
    SaleSummeryPeriod,
    SalesChannel,
)
from errors import ErrorMessages
from models import Category, InventoryLog, Product, Inventory, Sale
from fastapi import HTTPException
from schemas import (
    CategoryCreate,
    CategoryRead,
    InventoryUpdate,
    InventoryUpdateRead,
    LowStockRead,
    ProductCreate,
    ProductRead,
    InventoryCreate,
    InventoryRead,
    RevenueComparisonRead,
    SaleCreate,
    SaleRead,
)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def dashboard(db: Session = Depends(get_db)):
    total_categories = db.query(Category).count()
    total_products = db.query(Product).count()
    total_inventory_items = db.query(Inventory).count()
    total_sales = db.query(Sale).count()

    latest_sales = db.query(Sale).order_by(Sale.sale_date.desc()).limit(5).all()
    latest_sales_data = [
        {
            "id": sale.id,
            "product_id": sale.product_id,
            "quantity": sale.quantity,
            "total_price": sale.total_price,
            "channel": sale.channel,
            "sale_date": sale.sale_date,
        }
        for sale in latest_sales
    ]

    return {
        "message": "Welcome to the Inventory Management System",
        "summary": {
            "categories": total_categories,
            "products": total_products,
            "inventory_items": total_inventory_items,
            "sales": total_sales,
        },
        "latest_sales": latest_sales_data,
    }


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
        raise HTTPException(status_code=404, detail=ErrorMessages.CATEGORY_NOT_FOUND)
    return category


@app.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    db_inventory = Inventory(product_id=db_product.id, stock=1)
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
        raise HTTPException(status_code=404, detail=ErrorMessages.PRODUCT_NOT_FOUND)
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product or product.is_deleted:
        raise HTTPException(status_code=404, detail=ErrorMessages.PRODUCT_NOT_FOUND)
    product.is_deleted = True
    db.commit()
    return {"message": ErrorMessages.PRODUCT_SOFT_DELETED}


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
        raise HTTPException(status_code=404, detail=ErrorMessages.INVENTORY_NOT_FOUND)
    return inventory


@app.post("/sales/{product_id}", response_model=SaleRead)
def create_sale(product_id: int, sale: SaleCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PRODUCT_NOT_FOUND,
        )

    if product.inventory.stock >= Quantity.ONE.value:
        (product.inventory.stock - Quantity.ONE.value)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=InventoryStatus.OUT_OF_STOCK.value,
        )

    db_sale = Sale(
        product_id=product.id,
        quantity=Quantity.ONE.value,
        total_price=product.price,
        sale_date=datetime.utcnow(),
        channel=SalesChannel.OTHER.value,
        customer_email=None,
    )

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    return db_sale


@app.get("/sales/")
def get_sales(
    start_date: datetime = None,
    end_date: datetime = None,
    category_id: int = None,
    product_id: int = None,
    db: Session = Depends(get_db),
):
    query = db.query(Sale)

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if category_id:
        query = query.join(Sale.product).filter(Product.category_id == category_id)

    results = query.all()
    return [
        {
            "id": sale.id,
            "product_id": sale.product_id,
            "quantity": sale.quantity,
            "total_price": sale.total_price,
            "sale_date": sale.sale_date,
            "channel": sale.channel,
        }
        for sale in results
    ]


@app.get("/sales/summary/")
def revenue_summary(
    period: str = SaleSummeryPeriod.WEEKLY.value,
    db: Session = Depends(get_db),
):
    format_map = {
        SaleSummeryPeriod.DAILY.value: "%Y-%m-%d",
        SaleSummeryPeriod.WEEKLY.value: "%Y-%W",
        SaleSummeryPeriod.MONTHLY.value: "%Y-%m",
        SaleSummeryPeriod.ANNUAL.value: "%Y",
    }
    date_format = format_map.get(period, "%Y-%m-%d")

    data = (
        db.query(
            func.strftime(date_format, Sale.sale_date).label("period"),
            func.sum(Sale.total_price),
        )
        .group_by("period")
        .order_by("period")
        .all()
    )

    return [{"period": d[0], "total_revenue": d[1]} for d in data]


@app.get("/sales/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).get(sale_id)
    if not sale or sale.is_deleted:
        raise HTTPException(status_code=404, detail=ErrorMessages.SALE_NOT_FOUND)
    return sale 

@app.get(
        "/sales/comparison/", response_model=List[RevenueComparisonRead]
    )
def revenue_comparison(
    period: str = SaleSummeryPeriod.WEEKLY.value, db: Session = Depends(get_db)
):
    format_map = {
        SaleSummeryPeriod.DAILY.value: ("%Y-%m-%d", timedelta(days=1)),
        SaleSummeryPeriod.WEEKLY.value: ("%Y-%W", timedelta(weeks=1)),
        SaleSummeryPeriod.MONTHLY.value: ("%Y-%m", timedelta(days=30)),
        SaleSummeryPeriod.ANNUAL.value: ("%Y", timedelta(days=365)),
    }
    date_format, delta = format_map.get(period, ("%Y-%W", timedelta(weeks=1)))

    current_data = (
        db.query(
            func.strftime(date_format, Sale.sale_date).label("period"),
            func.sum(Sale.total_price).label("total_revenue"),
        )
        .group_by("period")
        .order_by("period")
        .all()
    )

    previous_data = (
        db.query(
            func.strftime(
                date_format, func.date(Sale.sale_date, f"-{delta.days} days")
            ).label("period"),
            func.sum(Sale.total_price).label("total_revenue"),
        )
        .group_by("period")
        .order_by("period")
        .all()
    )

    result = []
    for curr in current_data:
        curr_period, curr_revenue = curr
        prev_revenue = 0
        prev_period = curr_period
        for prev in previous_data:
            if prev[0] == curr_period:
                prev_revenue = prev[1]
                prev_period = prev[0]
                break
        percentage_change = (
            ((curr_revenue - prev_revenue) / prev_revenue * 100)
            if prev_revenue > 0
            else 0
        )
        result.append(
            {
                "current_period": curr_period,
                "current_revenue": curr_revenue,
                "previous_period": prev_period,
                "previous_revenue": prev_revenue,
                "percentage_change": percentage_change,
            }
        )

    return result


@app.get("/inventory/low-stock/", response_model=List[LowStockRead])
def get_low_stock(threshold: int = 5, db: Session = Depends(get_db)):
    low_stock_items = (
        db.query(Inventory)
        .join(Product, Inventory.product_id == Product.id)
        .filter(
            Inventory.stock <= threshold,
            Inventory.is_deleted == False,
            Product.is_deleted == False,
        )
        .all()
    )
    return [
        {
            "id": item.id,
            "product_id": item.product_id,
            "stock": item.stock,
            "product_name": item.product.name,
        }
        for item in low_stock_items
    ]


@app.put("/inventory/{inventory_id}", response_model=InventoryUpdateRead)
def update_inventory(
    inventory_id: int, update: InventoryUpdate, db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).get(inventory_id)
    if not inventory or inventory.is_deleted:
        raise HTTPException(status_code=404, detail=ErrorMessages.INVENTORY_NOT_FOUND)

    try:
        change_reason = (
            ChangeReason(update.change_reason)
            if update.change_reason
            else ChangeReason.MANUAL_ADJUSTMENT.value
        )
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid change_reason. Must be one of: {[e.value for e in ChangeReason]}",
        )

    if update.stock < 0:
        raise HTTPException(
            status_code=422, detail=ErrorMessages.STOCK_CANNOT_BE_NEGATIVE
        )

    log = InventoryLog(
        inventory_id=inventory.id,
        old_stock=inventory.stock,
        new_stock=update.stock,
        change_reason=change_reason,
        change_date=datetime.utcnow(),
    )
    db.add(log)

    inventory.stock = update.stock
    db.commit()
    db.refresh(inventory)

    return inventory


@app.get("/inventory/logs/", response_model=List[dict])
def get_inventory_logs(inventory_id: int = None, db: Session = Depends(get_db)):
    query = db.query(InventoryLog)
    if inventory_id:
        query = query.filter(InventoryLog.inventory_id == inventory_id)
    logs = query.all()
    return [
        {
            "id": log.id,
            "inventory_id": log.inventory_id,
            "old_stock": log.old_stock,
            "new_stock": log.new_stock,
            "change_reason": log.change_reason,
            "change_date": log.change_date,
        }
        for log in logs
    ]
