from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    """Customer model"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invoices = db.relationship('Invoice', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invoice_items = db.relationship('InvoiceItem', backref='product', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'stock': self.stock,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Invoice(db.Model):
    """Invoice model"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), default=0)
    shipping = db.Column(db.Numeric(10, 2), default=0)
    packing = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), default=0)
    received = db.Column(db.Numeric(10, 2), default=0)
    balance = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calculate subtotal, total and balance"""
        self.subtotal = sum(
            float(item.amount) for item in self.items
        ) if self.items else 0
        
        self.total = self.subtotal + float(self.shipping) + float(self.packing)
        self.balance = self.total - float(self.received)
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_no': self.invoice_no,
            'customer_id': self.customer_id,
            'customer': self.customer.to_dict() if self.customer else None,
            'subtotal': float(self.subtotal),
            'shipping': float(self.shipping),
            'packing': float(self.packing),
            'total': float(self.total),
            'received': float(self.received),
            'balance': float(self.balance),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class InvoiceItem(db.Model):
    """Invoice item model"""
    __tablename__ = 'invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=0)
    amount = db.Column(db.Numeric(10, 2))
    
    def calculate_amount(self):
        """Calculate item amount: (rate * qty) - discount"""
        self.amount = (float(self.rate) * self.qty) - float(self.discount)
        return float(self.amount)
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'qty': self.qty,
            'rate': float(self.rate),
            'discount': float(self.discount),
            'amount': float(self.amount) if self.amount else 0
        }
