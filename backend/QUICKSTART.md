# Quick Start Guide for Inventory Management System

## 📋 Pre-requisites

- Python 3.7+
- MySQL Server running locally or remotely
- pip (Python package manager)

## 🚀 Setup Steps

### Step 1: Install Python Packages

```bash
cd e:\Web-Projects\Python\1\Doc\backend
pip install -r requirements.txt
```

### Step 2: Create MySQL Database

Open MySQL Client or MySQL Workbench and run:

```sql
CREATE DATABASE inventory;
```

### Step 3: Configure Database Connection

Update `config.py` with your MySQL credentials:

```python
# Line 12 - For Development
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost/inventory"

# Example with root user
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_mysql_password@localhost/inventory"
```

### Step 4: Run the Application

```bash
python app.py
```

Output should show:
```
* Running on http://0.0.0.0:5000
* Debug mode: on
```

### Step 5: Test the API

In a new terminal:

```bash
# Option 1: Run the test script
python test_api.py

# Option 2: Test with curl
curl http://localhost:5000/

# Option 3: Use Postman/Insomnia
# Import the endpoints from README.md
```

## 📊 Project Structure

```
backend/
├── app.py                  # Main Flask app (entry point)
├── config.py              # Database & app configuration
├── models.py              # SQLAlchemy models (tables)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
├── README.md             # Full API documentation
├── test_api.py           # API testing script
├── routes/
│   ├── __init__.py
│   ├── products.py       # /api/products endpoints
│   ├── customers.py      # /api/customers endpoints
│   └── invoices.py       # /api/invoices endpoints
└── uploads/              # File upload directory
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Database URI**: MySQL connection string
- **Debug Mode**: True/False
- **Upload Folder**: Max file size (16MB default)
- **JSON Settings**: Sorting, formatting

Example custom config:

```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mypassword@localhost/inventory"
    SQLALCHEMY_ECHO = True  # Log SQL queries
```

## 🧪 Testing

### Test Script

```bash
# Install requests library if not already installed
pip install requests

# Run tests
python test_api.py
```

### Manual Testing with curl

```bash
# Create a product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 100, "stock": 5}'

# Get all products
curl http://localhost:5000/api/products

# Create a customer
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "mobile": "1234567890", "address": "123 Main St"}'

# Get all customers
curl http://localhost:5000/api/customers
```

### Using Postman

1. Create a new collection "Inventory API"
2. Add requests:
   - POST: http://localhost:5000/api/products
   - GET: http://localhost:5000/api/products
   - POST: http://localhost:5000/api/customers
   - GET: http://localhost:5000/api/customers
   - POST: http://localhost:5000/api/invoices
   - GET: http://localhost:5000/api/invoices

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Access denied for user 'root'@'localhost'"
- Check MySQL username and password in `config.py`
- Verify MySQL service is running
- Create/reset MySQL user:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Error: "Unknown database 'inventory'"
- Create the database:
```sql
CREATE DATABASE inventory;
```

### Port 5000 already in use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Error: pymysql
```bash
pip install pymysql
```

## 📱 Example Workflow

1. **Create a customer**
   ```bash
   POST /api/customers
   {"name": "Arijit Ray", "mobile": "9876543210"}
   ```

2. **Create products**
   ```bash
   POST /api/products
   {"name": "LUFFY GEAR 5", "price": 600, "stock": 10}
   ```

3. **Create an invoice**
   ```bash
   POST /api/invoices
   {
     "invoice_no": "AGG2713",
     "customer_id": 1,
     "shipping": 500,
     "packing": 2500,
     "items": [
       {
         "product_id": 1,
         "qty": 10,
         "rate": 600,
         "discount": 600
       }
     ]
   }
   ```

4. **Update payment received**
   ```bash
   PUT /api/invoices/1
   {"received": 6000}
   ```

5. **View invoice**
   ```bash
   GET /api/invoices/1
   ```

## 📈 Database Tables Created

The application automatically creates these tables on first run:

- `customers` - Customer information
- `products` - Product catalog
- `invoices` - Invoice records
- `invoice_items` - Line items in invoices

## 🌐 Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Using Apache + WSGI

Create `inventory.wsgi`:
```python
from app import create_app

application = create_app('production')
```

Configure Apache VirtualHost:
```apache
<VirtualHost *:80>
    ServerName inventory.example.com
    WSGIScriptAlias / /path/to/inventory.wsgi
    
    <Directory /path/to/backend>
        Require all granted
    </Directory>
</VirtualHost>
```

## 📞 Support

For issues or questions:
1. Check the full README.md
2. Review error messages
3. Verify database connection
4. Check MySQL server status

## 📝 Notes

- All monetary amounts use DECIMAL(10,2) for accuracy
- Datetime fields auto-populate with current timestamp
- Cascade delete removes related invoice items when invoice is deleted
- Balance is calculated automatically: total - received
- Totals are recalculated when invoice is updated

Enjoy! 🎉
