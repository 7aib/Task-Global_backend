from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enums import SalesChannel


class Config:
    from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config(Config):
        pass


class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category_id: Optional[int]


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    category: Optional[CategoryRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config(Config):
        pass


class InventoryBase(BaseModel):
    product_id: int
    stock: int = 0


class InventoryCreate(InventoryBase):
    pass


class InventoryRead(InventoryBase):
    id: int
    product: Optional[ProductRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config(Config):
        pass


class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    sale_date: Optional[datetime] = None
    channel: SalesChannel
    customer_email: Optional[EmailStr] = None


class SaleCreate(SaleBase):
    pass


class SaleRead(SaleBase):
    id: int
    product: Optional[ProductRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config(Config):
        pass
