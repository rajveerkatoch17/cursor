import sqlite3

# connect to database
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

query = """
SELECT 
    c.name AS customer_name,
    o.order_id,
    p.name AS product_name,
    oi.quantity,
    p.price,
    pay.status AS payment_status,
    (oi.quantity * p.price) AS total_amount
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN payments pay ON pay.order_id = o.order_id;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
