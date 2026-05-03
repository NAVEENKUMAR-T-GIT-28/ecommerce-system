# E-Commerce Management System

A full-stack database project that demonstrates **CRUD operations** using both a **Desktop GUI (Tkinter)** and a **Web Dashboard (Flask)** powered by a **MySQL database**.

---

## Features

### 🔹 Database (MySQL)

* Relational schema with normalization
* Foreign key relationships
* Tables:

  * Users
  * Products
  * Orders
  * Order Items
  * Payments

---

### 🔹 Desktop Application (Tkinter)

* Modern tab-based UI
* Full CRUD operations:

  * Create
  * Read
  * Update
  * Delete
* Table-wise data management
* Form-based data entry
* Real-time refresh

---

### 🔹 Web Application (Flask)

* Clean tab-based dashboard
* Displays all tables
* Advanced **JOIN Report**
* Summary analytics:

  * Total orders
  * Total spending per user

---

## Tech Stack

| Layer       | Technology     |
| ----------- | -------------- |
| Frontend    | HTML, CSS      |
| Backend     | Flask (Python) |
| Desktop App | Tkinter        |
| Database    | MySQL          |

---

## Project Structure

```bash
project/
│
├── app.py              # Flask web app
├── gui.py              # Tkinter CRUD application
├── templates/
│   └── index.html      # Web dashboard UI
├── database.sql        # Schema + insert values
└── README.md
```

---

## Setup Instructions

### 🔹 1. Clone Repository

```bash
git clone https://github.com/your-username/ecommerce-db-project.git
cd ecommerce-db-project
```

---

### 🔹 2. Setup Database

1. Open MySQL
2. Run:

```sql
CREATE DATABASE ecommerce_db;
USE ecommerce_db;
```

3. Import schema:

```bash
source database.sql;
```

---

### 🔹 3. Install Dependencies

You can install all required packages at once:

```bash
pip install -r requirements.txt
```

Alternatively, install them manually:

```bash
pip install flask mysql-connector-python python-dotenv
```

---

### 🔹 4. Run Flask App

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

### 🔹 5. Run Desktop GUI

```bash
python gui.py
```

---

## Key SQL Query (JOIN Report)

```sql
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
```

---

## Output Example

| User | Product    | Qty | Item Total | Order Total |
| ---- | ---------- | --- | ---------- | ----------- |
| Arun | Laptop     | 1   | 50000      | 53000       |
| Arun | Headphones | 2   | 3000       | 53000       |

---

## Learning Outcomes

* Database normalization
* SQL JOIN operations
* Full CRUD implementation
* GUI development using Tkinter
* Web development using Flask
* Multi-interface system design

---

## Architecture

```
Tkinter GUI   ─┐
               ├── MySQL Database
Flask Web App ─┘
```

---

## Author

**NAVEENKUMAR T**

---

## Notes

* Make sure MySQL is running
* Update DB credentials in code if needed
* Compatible with Python 3.8+

---

## Future Improvements

*  Authentication system
*  Data visualization (charts)
*  API integration
*  Responsive frontend

---

## License

This project is for academic and educational purposes.
