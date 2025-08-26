import config
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{config.DATABASE["username"]}:{config.DATABASE["password"]}@{config.DATABASE["db_host"]}/{config.DATABASE["db_name"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
