"""
API Testing Script
Run this to test all API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_products():
    """Test Product endpoints"""
    print("\n=== Testing Products ===")
    
    # Create product
    product_data = {
        "name": "LUFFY GEAR 5 WALKING FIGURE",
        "price": 600,
        "stock": 10
    }
    response = requests.post(f"{BASE_URL}/products", json=product_data)
    print(f"Create Product: {response.status_code}")
    product = response.json().get('product', {})
    product_id = product.get('id')
    print(json.dumps(response.json(), indent=2))
    
    # Get all products
    response = requests.get(f"{BASE_URL}/products")
    print(f"\nGet All Products: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Get specific product
    if product_id:
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        print(f"\nGet Product {product_id}: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        # Update product
        update_data = {"stock": 15}
        response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
        print(f"\nUpdate Product: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    
    return product_id

def test_customers():
    """Test Customer endpoints"""
    print("\n=== Testing Customers ===")
    
    # Create customer
    customer_data = {
        "name": "Arijit Ray",
        "mobile": "9876543210",
        "address": "123 Main Street, City"
    }
    response = requests.post(f"{BASE_URL}/customers", json=customer_data)
    print(f"Create Customer: {response.status_code}")
    customer = response.json().get('customer', {})
    customer_id = customer.get('id')
    print(json.dumps(response.json(), indent=2))
    
    # Get all customers
    response = requests.get(f"{BASE_URL}/customers")
    print(f"\nGet All Customers: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Get specific customer
    if customer_id:
        response = requests.get(f"{BASE_URL}/customers/{customer_id}")
        print(f"\nGet Customer {customer_id}: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        # Update customer
        update_data = {"mobile": "9876543211"}
        response = requests.put(f"{BASE_URL}/customers/{customer_id}", json=update_data)
        print(f"\nUpdate Customer: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    
    return customer_id

def test_invoices(customer_id, product_id):
    """Test Invoice endpoints"""
    print("\n=== Testing Invoices ===")
    
    if not customer_id or not product_id:
        print("Customer or Product not created. Skipping invoice tests.")
        return
    
    # Create invoice
    invoice_data = {
        "invoice_no": "AGG2713",
        "customer_id": customer_id,
        "shipping": 500,
        "packing": 2500,
        "received": 6000,
        "items": [
            {
                "product_id": product_id,
                "qty": 10,
                "rate": 600,
                "discount": 600
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/invoices", json=invoice_data)
    print(f"Create Invoice: {response.status_code}")
    invoice = response.json().get('invoice', {})
    invoice_id = invoice.get('id')
    print(json.dumps(response.json(), indent=2))
    
    # Get all invoices
    response = requests.get(f"{BASE_URL}/invoices")
    print(f"\nGet All Invoices: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Get specific invoice
    if invoice_id:
        response = requests.get(f"{BASE_URL}/invoices/{invoice_id}")
        print(f"\nGet Invoice {invoice_id}: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        # Update invoice (received amount)
        update_data = {"received": 8000}
        response = requests.put(f"{BASE_URL}/invoices/{invoice_id}", json=update_data)
        print(f"\nUpdate Invoice: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    
    # Get customer invoices
    response = requests.get(f"{BASE_URL}/invoices/customer/{customer_id}")
    print(f"\nGet Customer {customer_id} Invoices: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def main():
    """Run all tests"""
    print("Starting API Tests...")
    
    try:
        product_id = test_products()
        customer_id = test_customers()
        test_invoices(customer_id, product_id)
        
        print("\n=== All Tests Completed ===")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API. Make sure the server is running at http://localhost:5000")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()
