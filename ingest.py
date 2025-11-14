import sqlite3
import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ecommerce.db')

CSV_FILES = {
    'customers': os.path.join(BASE_DIR, 'customers.csv'),
    'products': os.path.join(BASE_DIR, 'products.csv'),
    'orders': os.path.join(BASE_DIR, 'orders.csv'),
    'order_items': os.path.join(BASE_DIR, 'order_items.csv'),
    'payments': os.path.join(BASE_DIR, 'payments.csv'),
}


def read_csv_rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def create_tables(conn):
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')

    # Drop if exist to make script idempotent
    cur.executescript('''
    DROP TABLE IF EXISTS payments;
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    ''')

    cur.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE payments (
        payment_id TEXT PRIMARY KEY,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )
    ''')

    conn.commit()


def insert_data(conn):
    cur = conn.cursor()

    # Customers
    cust_rows = read_csv_rows(CSV_FILES['customers'])
    cust_tuples = []
    for r in cust_rows:
        cid = int(r['id'])
        name = r['name']
        email = r['email']
        cust_tuples.append((cid, name, email))
    cur.executemany('INSERT INTO customers (id, name, email) VALUES (?, ?, ?)', cust_tuples)

    # Products
    prod_rows = read_csv_rows(CSV_FILES['products'])
    prod_tuples = []
    for r in prod_rows:
        pid = int(r['id'])
        name = r['name']
        category = r.get('category')
        price = float(r['price']) if r.get('price') else 0.0
        prod_tuples.append((pid, name, category, price))
    cur.executemany('INSERT INTO products (id, name, category, price) VALUES (?, ?, ?, ?)', prod_tuples)

    # Orders
    order_rows = read_csv_rows(CSV_FILES['orders'])
    order_tuples = []
    for r in order_rows:
        oid = int(r['order_id'])
        cid = int(r['customer_id'])
        date = r.get('date')
        order_tuples.append((oid, cid, date))
    cur.executemany('INSERT INTO orders (order_id, customer_id, date) VALUES (?, ?, ?)', order_tuples)

    # Order items
    oi_rows = read_csv_rows(CSV_FILES['order_items'])
    oi_tuples = []
    for r in oi_rows:
        oid = int(r['order_id'])
        pid = int(r['product_id'])
        qty = int(r['quantity'])
        oi_tuples.append((oid, pid, qty))
    cur.executemany('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', oi_tuples)

    # Payments
    pay_rows = read_csv_rows(CSV_FILES['payments'])
    pay_tuples = []
    for r in pay_rows:
        pay_id = r['payment_id']
        oid = int(r['order_id'])
        amt = float(r['amount']) if r.get('amount') else 0.0
        status = r.get('status') or ''
        pay_tuples.append((pay_id, oid, amt, status))
    cur.executemany('INSERT INTO payments (payment_id, order_id, amount, status) VALUES (?, ?, ?, ?)', pay_tuples)

    conn.commit()


def report_counts(conn):
    cur = conn.cursor()
    tables = ['customers', 'products', 'orders', 'order_items', 'payments']
    for t in tables:
        cur.execute(f'SELECT COUNT(*) FROM {t}')
        count = cur.fetchone()[0]
        print(f"{t}: {count}")


def main():
    # Check CSVs exist
    missing = [name for name, path in CSV_FILES.items() if not os.path.exists(path)]
    if missing:
        print('Missing CSV files:', missing)
        sys.exit(1)

    if os.path.exists(DB_PATH):
        print('Overwriting existing database at', DB_PATH)
        try:
            os.remove(DB_PATH)
        except Exception as e:
            print('Could not remove existing DB file:', e)
            sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        insert_data(conn)
        print('Import complete. Database created at:', DB_PATH)
        report_counts(conn)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
