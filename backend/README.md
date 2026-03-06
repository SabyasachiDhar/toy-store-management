# Inventory Management System

A Flask-based REST API for managing products, customers, and invoices with MySQL database.

## Features

- ✅ Product Management (Create, Read, Update, Delete)
- ✅ Customer Management (Create, Read, Update, Delete)
- ✅ Invoice Management with automatic calculations
- ✅ Invoice Items with quantity, rate, and discount
- ✅ Automatic total and balance calculations
- ✅ MySQL database with proper relationships
- ✅ RESTful API endpoints
- ✅ Error handling and validation

## Folder Structure

```
inventory-api/
├── app.py                    # Flask application factory
├── config.py                 # Configuration management
├── models.py                 # SQLAlchemy models
├── requirements.txt          # Python dependencies
├── routes/
│   ├── __init__.py
│   ├── products.py          # Product routes
│   ├── customers.py         # Customer routes
│   └── invoices.py          # Invoice routes
├── uploads/                  # File upload directory
└── README.md                # Documentation
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database

```sql
CREATE DATABASE inventory;
```

### 3. Configure Database

Edit `config.py` and update the database connection string:

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/inventory"
```

Example:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/inventory"
```

## Running the Application

### Development

```bash
python app.py
```

The API will run at `http://localhost:5000`

### Production

```bash
export FLASK_ENV=production
python app.py
```

Or with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## API Endpoints

### Products

- **POST** `/api/products` - Create a product
- **GET** `/api/products` - Get all products
- **GET** `/api/products/<id>` - Get a specific product
- **PUT** `/api/products/<id>` - Update a product
- **DELETE** `/api/products/<id>` - Delete a product

### Customers

- **POST** `/api/customers` - Create a customer
- **GET** `/api/customers` - Get all customers
- **GET** `/api/customers/<id>` - Get a specific customer
- **PUT** `/api/customers/<id>` - Update a customer
- **DELETE** `/api/customers/<id>` - Delete a customer

### Invoices

- **POST** `/api/invoices` - Create an invoice
- **GET** `/api/invoices` - Get all invoices
- **GET** `/api/invoices/<id>` - Get a specific invoice
- **PUT** `/api/invoices/<id>` - Update an invoice
- **DELETE** `/api/invoices/<id>` - Delete an invoice
- **GET** `/api/invoices/customer/<customer_id>` - Get customer invoices
- **POST** `/api/invoices/<id>/items` - Add item to invoice
- **DELETE** `/api/invoices/items/<item_id>` - Delete invoice item

## Example Usage

### 1. Create a Product

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "LUFFY GEAR 5 WALKING FIGURE",
    "price": 600,
    "stock": 10
  }'
```

Response:
```json
{
  "message": "Product added successfully",
  "product": {
    "id": 1,
    "name": "LUFFY GEAR 5 WALKING FIGURE",
    "price": 600.0,
    "stock": 10,
    "created_at": "2026-03-06T12:00:00"
  }
}
```

### 2. Create a Customer

```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Arijit Ray",
    "mobile": "9876543210",
    "address": "123 Main St, City"
  }'
```

Response:
```json
{
  "message": "Customer added successfully",
  "customer": {
    "id": 1,
    "name": "Arijit Ray",
    "mobile": "9876543210",
    "address": "123 Main St, City",
    "created_at": "2026-03-06T12:00:00"
  }
}
```

### 3. Create an Invoice

```bash
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_no": "AGG2713",
    "customer_id": 1,
    "shipping": 500,
    "packing": 2500,
    "received": 6000,
    "items": [
      {
        "product_id": 1,
        "qty": 10,
        "rate": 600,
        "discount": 600
      }
    ]
  }'
```

Response:
```json
{
  "message": "Invoice created successfully",
  "invoice": {
    "id": 1,
    "invoice_no": "AGG2713",
    "customer_id": 1,
    "customer": {...},
    "subtotal": 5400.0,
    "shipping": 500.0,
    "packing": 2500.0,
    "total": 8400.0,
    "received": 6000.0,
    "balance": 2400.0,
    "items": [...],
    "created_at": "2026-03-06T12:00:00"
  }
}
```

### 4. Get Customer Invoices

```bash
curl http://localhost:5000/api/invoices/customer/1
```

### 5. Update Payment Received

```bash
curl -X PUT http://localhost:5000/api/invoices/1 \
  -H "Content-Type: application/json" \
  -d '{
    "received": 10000
  }'
```

## Database Schema

### customers
```sql
CREATE TABLE customers (
   id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   mobile VARCHAR(20),
   address TEXT,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### products
```sql
CREATE TABLE products (
   id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(200) NOT NULL,
   price DECIMAL(10,2) NOT NULL,
   stock INT DEFAULT 0,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### invoices
```sql
CREATE TABLE invoices (
   id INT AUTO_INCREMENT PRIMARY KEY,
   invoice_no VARCHAR(50) UNIQUE NOT NULL,
   customer_id INT NOT NULL,
   subtotal DECIMAL(10,2) DEFAULT 0,
   shipping DECIMAL(10,2) DEFAULT 0,
   packing DECIMAL(10,2) DEFAULT 0,
   total DECIMAL(10,2) DEFAULT 0,
   received DECIMAL(10,2) DEFAULT 0,
   balance DECIMAL(10,2) DEFAULT 0,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY(customer_id) REFERENCES customers(id)
);
```

### invoice_items
```sql
CREATE TABLE invoice_items (
   id INT AUTO_INCREMENT PRIMARY KEY,
   invoice_id INT NOT NULL,
   product_id INT NOT NULL,
   qty INT NOT NULL,
   rate DECIMAL(10,2) NOT NULL,
   discount DECIMAL(10,2) DEFAULT 0,
   amount DECIMAL(10,2),
   FOREIGN KEY(invoice_id) REFERENCES invoices(id),
   FOREIGN KEY(product_id) REFERENCES products(id)
);
```

## Calculation Details

### Invoice Totals

- **Subtotal**: Sum of all item amounts
- **Item Amount**: (rate × qty) - discount
- **Total**: subtotal + shipping + packing
- **Balance**: total - received

Example (from AGG2713):
```
Item: 10 × ₹600 - ₹600 = ₹5,400 (subtotal)
Shipping: ₹500
Packing: ₹2,500
Total: ₹8,400
Received: ₹6,000
Balance: ₹2,400
```

## Configuration Environments

### Development
- Debug: True
- Database: mysql+pymysql://root:password@localhost/inventory

### Production
- Debug: False
- Database: mysql+pymysql://user:password@localhost/inventory

### Testing
- SQLite in-memory database

Set environment:
```bash
export FLASK_ENV=production
python app.py
```

## Error Handling

All endpoints return standardized error responses:

```json
{
  "error": "Error message here"
}
```

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 404: Not Found
- 500: Internal Server Error

## Future Enhancements

- File uploads for invoices/receipts
- PDF invoice generation
- Email notifications
- Inventory tracking
- User authentication
- Pagination for large datasets
- Advanced filtering and search
- Invoice status tracking (draft, paid, etc.)
- Discount management
- Tax calculations

## License

MIT
