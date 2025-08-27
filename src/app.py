from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:1234@localhost/ecommerce_api"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
