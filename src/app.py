from .app_config import app, db
from .api import users_api
from .api import products_api
from .api import orders_api

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    app.run(debug=True)