from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import config
from models.base import Base
from models.user import User
from models.order import Order
from models.product import Product

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{config.DATABASE["username"]}:{config.DATABASE["password"]}@{config.DATABASE["db_host"]}/{config.DATABASE["db_name"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
