-- =========================
-- E-COMMERCE DATABASE
-- =========================
DROP DATABASE IF EXISTS ecommerce_db;
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(20)
);

-- =========================
-- PRODUCTS TABLE
-- =========================
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(8,2),
    stock INT
);

-- =========================
-- ORDERS TABLE
-- =========================
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME,
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- ORDER ITEMS TABLE
-- =========================
CREATE TABLE order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- =========================
-- PAYMENTS TABLE
-- =========================
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    amount DECIMAL(8,2),
    method VARCHAR(20),
    status VARCHAR(20),
    paid_at DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- =========================
-- INSERT USERS
-- =========================
INSERT INTO users (username, full_name, email, phone, role) VALUES
('arun','Arun Kumar','arun@gmail.com','9876543210','customer'),
('divya','Divya Nair','divya@gmail.com','9876501234','customer'),
('admin','Admin User','admin@gmail.com','9999999999','admin');

-- =========================
-- INSERT PRODUCTS
-- =========================
INSERT INTO products (name, category, price, stock) VALUES
('Laptop','Electronics',50000.00,10),
('Mobile','Electronics',20000.00,20),
('Headphones','Accessories',1500.00,50),
('Keyboard','Accessories',800.00,30);

-- =========================
-- INSERT ORDERS
-- =========================
INSERT INTO orders (user_id, order_date, status) VALUES
(1,'2026-05-01 10:30:00','placed'),
(2,'2026-05-02 12:00:00','placed');

-- =========================
-- INSERT ORDER ITEMS
-- =========================
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1,1,1),
(1,3,2),
(2,2,1);

-- =========================
-- INSERT PAYMENTS
-- =========================
INSERT INTO payments (order_id, amount, method, status, paid_at) VALUES
(1,53000.00,'card','success','2026-05-01 11:00:00'),
(2,20000.00,'upi','success','2026-05-02 12:30:00');

-- =========================
-- SAMPLE SELECT QUERIES
-- =========================
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT * FROM payments;

-- =========================
-- JOIN REPORT
-- =========================
SELECT 
u.username,
o.order_id,
p.name AS product_name,
oi.quantity,
p.price,
(p.price * oi.quantity) AS item_total,
pay.amount AS order_total,
o.status,
pay.method,
pay.paid_at
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN payments pay ON o.order_id = pay.order_id;

-- =========================
-- SUMMARY REPORT
-- =========================
SELECT 
u.username,
COUNT(o.order_id) AS total_orders,
SUM(pay.amount) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN payments pay ON o.order_id = pay.order_id
GROUP BY u.username;