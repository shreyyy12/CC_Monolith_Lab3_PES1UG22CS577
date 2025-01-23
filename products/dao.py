import os
import sqlite3


def connect(path):
    exists = os.path.exists(path)
    __conn = sqlite3.connect(path)
    if not exists:
        create_tables(__conn)
    
    __conn.row_factory = sqlite3.Row
    return __conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL,
            qty INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    
    # Insert default data if tables were created
    conn.executemany("""
        INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)
    """, [
        ('Backpack', 'A durable and stylish backpack for daily use.', 800.0, 10),
        ('Wireless Mouse', 'A sleek and ergonomic wireless mouse with a long battery life.', 800.0, 20),
        ('Bluetooth Speaker', 'A portable Bluetooth speaker with high-quality sound and deep bass.', 3000.0, 30),
        ('Laptop Stand', 'An adjustable laptop stand for better posture and cooling.', 250.0, 15),
        ('Notebook', 'A premium notebook with thick, high-quality paper.', 50.0, 50),
        ('Smartphone Case', 'A durable and stylish case for protecting your smartphone.', 150.0, 25),
        ('Power Bank', 'A high-capacity power bank with fast charging support.', 900.0, 20),
        ('Headphones', 'Over-ear headphones with noise cancellation and deep bass.', 5000.0, 10),
        ('Gaming Keyboard', 'A mechanical gaming keyboard with RGB lighting.', 3000.0, 10),
        ('USB-C Hub', 'A multi-port USB-C hub for all your connectivity needs.', 400.0, 25),
        ('Fitness Tracker', 'A sleek fitness tracker with heart rate monitoring.', 1000.0, 20),
        ('Travel Mug', 'An insulated travel mug that keeps your drinks hot or cold.', 500.0, 30),
        ('Desk Organizer', 'A compact desk organizer for keeping your workspace tidy.', 1200.0, 40),
        ('External Hard Drive', 'A portable external hard drive with 1TB of storage.', 800.0, 15),
        ('Wireless Charger', 'A fast wireless charger compatible with most devices.', 2500.0, 30),
        ('Digital Camera', 'A compact digital camera with 4K video recording.', 20000.0, 5),
        ('Electric Kettle', 'A fast-boiling electric kettle with auto shut-off.', 3000.0, 20),
        ('Smart Watch', 'A stylish smartwatch with fitness and notification features.', 12000.0, 10),
        ('LED Desk Lamp', 'A modern LED desk lamp with adjustable brightness.', 2000.0, 35),
        ('Portable Projector', 'A mini portable projector with HD resolution.', 15000.0, 8)
    ])
    conn.commit()


def fetch_all_products(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    return cursor.fetchall()


def list_products():
    conn = connect('products.db')
    products = fetch_all_products(conn)
    conn.close()
    
    if products:
        products.sort(key=lambda x: x['id'])  # Sorting based on 'id' (or another key as required)
    return products


def add_product(product: dict):
    conn = connect('products.db')
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, description, cost, qty) VALUES (?, ?, ?, ?)',
                       (product['name'], product['description'], product['cost'], product['qty']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding product: {e}")
    finally:
        conn.close()


def get_product(product_id: int):
    conn = connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    
    conn = connect('products.db')
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET qty = ? WHERE id = ?', (qty, product_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating quantity: {e}")
    finally:
        conn.close()


def delete_product(product_id: int):
    conn = connect('products.db')
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting product: {e}")
    finally:
        conn.close()


def update_product(product_id: int, product: dict):
    conn = connect('products.db')
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET name = ?, description = ?, cost = ?, qty = ? WHERE id = ?',
                       (product['name'], product['description'], product['cost'], product['qty'], product_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating product: {e}")
    finally:
        conn.close()

