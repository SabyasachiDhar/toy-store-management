from flask import Blueprint, request, jsonify
from models import db, Customer
from sqlalchemy.exc import SQLAlchemyError

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['POST'])
def add_customer():
    """Add a new customer"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('name'):
            return jsonify({'error': 'Missing required field: name'}), 400
        
        customer = Customer(
            name=data['name'],
            mobile=data.get('mobile'),
            address=data.get('address')
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer added successfully',
            'customer': customer.to_dict()
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        customers = Customer.query.all()
        return jsonify({
            'count': len(customers),
            'customers': [c.to_dict() for c in customers]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a specific customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update a customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            customer.name = data['name']
        if 'mobile' in data:
            customer.mobile = data['mobile']
        if 'address' in data:
            customer.address = data['address']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Customer updated successfully',
            'customer': customer.to_dict()
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({'message': 'Customer deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
