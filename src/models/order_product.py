from sqlalchemy import ForeignKey, Table, Column
from .base import Base

order_product = Table(
    "order_procuct",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)