from flask import Flask, render_template
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from contextlib import contextmanager

app = Flask(__name__)

@contextmanager
def get_db():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'ecommerce_db')
    )
    try:
        yield conn
    finally:
        conn.close()

def fetch(query):
    with get_db() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(query)
        return cur.fetchall()

@app.route('/')
def home():
    data = {
        "users": fetch("SELECT * FROM users"),
        "products": fetch("SELECT * FROM products"),
        "orders": fetch("SELECT * FROM orders"),
        "order_items": fetch("SELECT * FROM order_items"),
        "payments": fetch("SELECT * FROM payments"),

        # JOIN REPORT
        "join": fetch("""
            SELECT 
            u.username,
            o.order_id,
            p.name AS product_name,
            oi.quantity,
            p.price,

            -- per product total
            (p.price * oi.quantity) AS item_total,

            -- full order amount
            pay.amount AS order_total,

            o.status,
            pay.method,
            pay.paid_at

            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            JOIN payments pay ON o.order_id = pay.order_id

            ORDER BY o.order_id
        """),

        # ADVANCED REPORT
        "summary": fetch("""
            SELECT 
            u.username,
            COUNT(o.order_id) AS total_orders,
            SUM(pay.amount) AS total_spent
            FROM users u
            JOIN orders o ON u.user_id = o.user_id
            JOIN payments pay ON o.order_id = pay.order_id
            GROUP BY u.username
        """)
    }
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)