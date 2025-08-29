from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.base import Base
from config import DATABASE

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["db_host"]}/{DATABASE["db_name"]}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)
