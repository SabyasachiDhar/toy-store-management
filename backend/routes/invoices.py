from flask import Blueprint, request, jsonify
from models import db, Invoice, InvoiceItem, Product, Customer
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('/invoices', methods=['POST'])
def create_invoice():
    """Create a new invoice with items"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('invoice_no') or not data.get('customer_id'):
            return jsonify({'error': 'Missing required fields: invoice_no, customer_id'}), 400
        
        if not data.get('items') or not isinstance(data['items'], list):
            return jsonify({'error': 'Missing or invalid items array'}), 400
        
        # Check if customer exists
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        # Check if invoice_no already exists
        existing = Invoice.query.filter_by(invoice_no=data['invoice_no']).first()
        if existing:
            return jsonify({'error': 'Invoice number already exists'}), 400
        
        # Create invoice
        invoice = Invoice(
            invoice_no=data['invoice_no'],
            customer_id=data['customer_id'],
            shipping=data.get('shipping', 0),
            packing=data.get('packing', 0),
            received=data.get('received', 0)
        )
        
        # Add items
        for item_data in data['items']:
            if not item_data.get('product_id') or not item_data.get('qty') or not item_data.get('rate'):
                return jsonify({'error': 'Each item must have: product_id, qty, rate'}), 400
            
            product = Product.query.get(item_data['product_id'])
            if not product:
                return jsonify({'error': f"Product {item_data['product_id']} not found"}), 404
            
            item = InvoiceItem(
                product_id=item_data['product_id'],
                qty=item_data['qty'],
                rate=item_data['rate'],
                discount=item_data.get('discount', 0)
            )
            item.calculate_amount()
            invoice.items.append(item)
        
        # Calculate totals
        invoice.calculate_totals()
        
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice created successfully',
            'invoice': invoice.to_dict()
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/invoices', methods=['GET'])
def get_invoices():
    """Get all invoices"""
    try:
        invoices = Invoice.query.all()
        return jsonify({
            'count': len(invoices),
            'invoices': [inv.to_dict() for inv in invoices]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get a specific invoice"""
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        return jsonify(invoice.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """Update invoice (received amount, shipping, packing)"""
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        data = request.get_json()
        
        if 'received' in data:
            invoice.received = data['received']
        if 'shipping' in data:
            invoice.shipping = data['shipping']
        if 'packing' in data:
            invoice.packing = data['packing']
        
        # Recalculate totals
        invoice.calculate_totals()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice updated successfully',
            'invoice': invoice.to_dict()
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Delete an invoice"""
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        db.session.delete(invoice)
        db.session.commit()
        
        return jsonify({'message': 'Invoice deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoices_bp.route('/invoices/customer/<int:customer_id>', methods=['GET'])
def get_customer_invoices(customer_id):
    """Get all invoices for a specific customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        invoices = Invoice.query.filter_by(customer_id=customer_id).all()
        return jsonify({
            'count': len(invoices),
            'customer': customer.to_dict(),
            'invoices': [inv.to_dict() for inv in invoices]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@invoices_bp.route('/invoices/<int:invoice_id>/items', methods=['POST'])
def add_invoice_item(invoice_id):
    """Add an item to an existing invoice"""
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        data = request.get_json()
        
        if not data.get('product_id') or not data.get('qty') or not data.get('rate'):
            return jsonify({'error': 'Missing required fields: product_id, qty, rate'}), 400
        
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        item = InvoiceItem(
            invoice_id=invoice_id,
            product_id=data['product_id'],
            qty=data['qty'],
            rate=data['rate'],
            discount=data.get('discount', 0)
        )
        item.calculate_amount()
        
        db.session.add(item)
        invoice.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to invoice',
            'invoice': invoice.to_dict()
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/invoices/items/<int:item_id>', methods=['DELETE'])
def delete_invoice_item(item_id):
    """Delete an item from an invoice"""
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Invoice item not found'}), 404
        
        invoice = item.invoice
        db.session.delete(item)
        invoice.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Item deleted from invoice',
            'invoice': invoice.to_dict()
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
