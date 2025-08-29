from app_config import app, db
import api.users_api
import api.products_api
import api.orders_api

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    app.run(debug=True)