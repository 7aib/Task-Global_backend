from sqlalchemy import Column, Integer, String, Enum as SQLAEnum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from enums import SalesChannel
from mixins import TimestampMixin, SoftDeleteMixin

Base = declarative_base()


class Category(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")


class Product(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sales = relationship("Sale", back_populates="product")


class Inventory(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    stock = Column(Integer, default=0)

    product = relationship("Product", back_populates="inventory")


class Sale(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)
    channel = Column(
        SQLAEnum(SalesChannel, name="saleschannel", native_enum=False),
        nullable=False,
        default=SalesChannel.OTHER,
    )
    customer_email = Column(String, nullable=True)

    product = relationship("Product", back_populates="sales")
