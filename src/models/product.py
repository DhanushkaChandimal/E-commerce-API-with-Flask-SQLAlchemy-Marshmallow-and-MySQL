from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float
from typing import List
from .base import Base
from .order_product import order_product

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] =  mapped_column(Float)
    
    orders: Mapped[List["Order"]] = relationship("Order", secondary=order_product, back_populates="products") # type: ignore
