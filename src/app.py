from flask import request, jsonify
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Float, Table, Column, select, exc
from marshmallow import ValidationError
from datetime import datetime
from typing import List
from config import Base, app, db, ma

order_product = Table(
    "order_procuct",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)

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
    
    products: Mapped[List["Product"]] = relationship("Product", secondary=order_product, back_populates="orders")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] =  mapped_column(Float)
    
    orders: Mapped[List["Order"]] = relationship("Order", secondary=order_product, back_populates="products")

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# ======================User endpoints======================

@app.route('/users', methods = ['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200

@app.route('/users/<int:id>', methods = ['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

@app.route('/users', methods = ['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@app.route('/users/<int:id>', methods = ['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data['name']
    user.address = user_data['address']
    user.email = user_data['email']
    db.session.commit()
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {id}"}), 200

# ======================Product endpoints======================

@app.route('/products', methods = ['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products_schema.jsonify(products), 200

@app.route('/products/<int:id>', methods = ['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200

@app.route('/products', methods = ['POST'])
def create_product():
    try:
        print("=============================")
        print(request.json)
        product_data = product_schema.load(request.json)
        print(product_data)
        print("=============================")
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@app.route('/products/<int:id>', methods = ['PUT'])
def update_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product.product_name = product_data['product_name']
    product.price = product_data['price']
    db.session.commit()
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>', methods = ['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted product {id}"}), 200

# ======================Order endpoints======================

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

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    app.run(debug=True)