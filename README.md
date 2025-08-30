# E-Commerce API

A RESTful API for managing users, products, and orders in an e-commerce platform. Built with Flask, SQLAlchemy, Marshmallow, and JWT authentication.

---

## Features

- **User Management:** Create, read, update, delete users (JWT protected)
- **Product Management:** Create, update, delete products and get products with pagination and sorting
- **Order Management:** Create, view, update, and delete orders; advanced endpoints for order-product relationships
- **JWT Authentication:** Secure user operations with token-based authentication

---

## Folder Structure

```
src/
│   app.py
│   app_config.py
│   config.py
│   schemas.py
│
├── api/
│   ├── users_api.py
│   ├── products_api.py
│   └── orders_api.py
│
└── models/
    ├── base.py
    ├── user.py
    ├── product.py
    ├── order.py
    └── order_product.py
```

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/DhanushkaChandimal/E-commerce-API-with-Flask-SQLAlchemy-Marshmallow-and-MySQL.git
```

### 2. Set Up a Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# Or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Database and Auth

Edit `src/config.py` and update with your own credentials:

```python
DATABASE = {
    "db_name": "ecommerce_api",
    "db_host": "localhost",
    "username": "root",
    "password": "<db-password>"
}

AUTH = {
    "email": "<admin-email>",
    "password": "<admin-password>",
    "JWT_SECRET_KEY": "<secret-key>"
}
```

### 5. Initialize the Database

Uncomment these lines in `src/app.py` to create tables:
```python
with app.app_context():
    db.create_all()
```
Run the app once, then comment these lines again.

### 6. Run the Application

From the project root (the folder containing `src`), run:
```sh
python -m src.app
```
The API will be available at `http://localhost:5000/`.

---

## Usage

### Authentication

1. **Login to get JWT token:**
   - `POST /login`
   - Body:
     ```json
     {
       "email": "<admin-email>",
       "password": "<admin-password>"
     }
     ```
   - Copy the `access_token` from the response.

2. **Access protected endpoints:**
   - Add header to your requests:
     ```
     Authorization: Bearer <access_token>
     ```

### Example Endpoints

- `GET /products?page=1&per_page=10&sort_by=price&sort=asc` (JWT required)
- `POST /login`
- `GET /users` (JWT required)
- `GET /orders/user/<user_id>
- `PUT /orders/<order_id>/status`

---

## Advanced Features

- **Pagination:** `/products?page=2&per_page=5`
- **Sorting:** `/products?sort_by=price&sort=desc`
- **Order Management:** View products in an order, remove products from an order

---

## Notes

- Make sure your MySQL server is running and accessible with the credentials in `config.py`.
- For JWT authentication, use the `/login` endpoint to obtain a token.
- Only get users endpoint is protected and require a valid JWT token.
