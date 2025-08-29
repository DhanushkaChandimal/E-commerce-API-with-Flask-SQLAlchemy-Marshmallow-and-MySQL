from flask import request, jsonify
from sqlalchemy import select, exc
from marshmallow import ValidationError
from app_config import app, db
from models.user import User
from models.order import Order
from models.product import Product
from schemas import products_schema, order_schema, orders_schema

@app.route('/orders', methods = ['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json)
        new_order = Order(user_id=order_data['user_id'], order_date=order_data['order_date'])
        db.session.add(new_order)
        db.session.commit()
    except ValidationError as e:
        return jsonify(e.messages), 400
    except exc.IntegrityError:
        return jsonify({"message": "Invalid user ID"}), 400
    return order_schema.jsonify(new_order), 201

@app.route('/orders/<order_id>/add_product/<product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    try:
        order.products.append(product)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": f"Product {product.id} is already in the list"}), 400

    return jsonify({"message": f"{product.product_name} add to the order {order.id}."}), 200

@app.route('/orders/<order_id>/remove_product/<product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    if not product in order.products:
        return jsonify({"message": f"Product {product.id} is not in the order {order.id}"}), 400

    order.products.remove(product)
    db.session.commit()
    return jsonify({"message": f"{product.product_name} deleted from the order {order.id}."}), 200

@app.route('/orders/user/<user_id>', methods = ['GET'])
def get_all_orders_for_user(user_id):
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    query = select(Order).filter(Order.user_id == user_id)
    orders = db.session.execute(query).scalars().all()
    return orders_schema.jsonify(orders), 200

@app.route('/orders/<order_id>/products', methods = ['GET'])
def get_all_products_for_order(order_id):
    order = db.session.get(Order, order_id)
    return jsonify({"products": products_schema.dump(order.products)}), 200