-- Inventory Management System Database Schema
-- Run this script to create the database and tables manually

-- Create Database
CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
   id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   mobile VARCHAR(20),
   address TEXT,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Products Table
CREATE TABLE IF NOT EXISTS products (
   id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(200) NOT NULL,
   price DECIMAL(10,2) NOT NULL,
   stock INT DEFAULT 0,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Invoices Table
CREATE TABLE IF NOT EXISTS invoices (
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
   FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
   INDEX idx_invoice_no (invoice_no),
   INDEX idx_customer_id (customer_id),
   INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Invoice Items Table
CREATE TABLE IF NOT EXISTS invoice_items (
   id INT AUTO_INCREMENT PRIMARY KEY,
   invoice_id INT NOT NULL,
   product_id INT NOT NULL,
   qty INT NOT NULL,
   rate DECIMAL(10,2) NOT NULL,
   discount DECIMAL(10,2) DEFAULT 0,
   amount DECIMAL(10,2),
   FOREIGN KEY(invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
   FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE RESTRICT,
   INDEX idx_invoice_id (invoice_id),
   INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample Data (Optional)

-- Insert Sample Customers
INSERT INTO customers (name, mobile, address) VALUES
('Arijit Ray', '9876543210', '123 Main Street, Mumbai'),
('Rajesh Kumar', '9876543211', '456 Park Avenue, Delhi'),
('Priya Singh', '9876543212', '789 Raj Path, Bangalore');

-- Insert Sample Products
INSERT INTO products (name, price, stock) VALUES
('LUFFY GEAR 5 WALKING FIGURE', 600, 10),
('NARUTO ACTION FIGURE', 500, 15),
('ONE PIECE COLLECTIBLE', 800, 8),
('DRAGON BALL Z STATUE', 750, 12);

-- Insert Sample Invoice
-- (Note: Adjust customer_id if needed)
INSERT INTO invoices (
   invoice_no,
   customer_id,
   subtotal,
   shipping,
   packing,
   total,
   received,
   balance
) VALUES
('AGG2713', 1, 5400, 500, 2500, 8400, 6000, 2400);

-- Insert Sample Invoice Items
-- (Note: Adjust invoice_id and product_id if needed)
INSERT INTO invoice_items (
   invoice_id,
   product_id,
   qty,
   rate,
   discount,
   amount
) VALUES
(1, 1, 10, 600, 600, 5400),
(1, 2, 2, 500, 0, 1000);

-- Verify Data
SELECT 'Customers:' AS section;
SELECT * FROM customers;

SELECT 'Products:' AS section;
SELECT * FROM products;

SELECT 'Invoices:' AS section;
SELECT * FROM invoices;

SELECT 'Invoice Items:' AS section;
SELECT * FROM invoice_items;
