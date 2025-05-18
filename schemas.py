from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enums import ChangeReason, SalesChannel


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


class RevenueComparisonRead(BaseModel):
    current_period: str
    current_revenue: float
    previous_period: str
    previous_revenue: float
    percentage_change: float

    class Config(Config):
        pass


class LowStockRead(BaseModel):
    id: int
    product_id: int
    stock: int
    product_name: str

    class Config(Config):
        pass


class InventoryUpdate(BaseModel):
    stock: int
    change_reason: ChangeReason


class InventoryUpdateRead(BaseModel):
    id: int
    product_id: int
    stock: int
    is_deleted: bool

    class Config(Config):
        pass
