Cursor A-SDLC E-Commerce Project
Synthetic Data • SQLite Ingestion • Multi-Table SQL Joins

This project was created as part of the A-SDLC (Agent Software Development Life Cycle) exercise using Cursor IDE.
It demonstrates synthetic dataset generation, structured ingestion into SQLite, and multi-table SQL queries — all automated through agent-driven development.
📁Cursor
│
├── customers.csv
├── products.csv
├── orders.csv
├── order_items.csv
├── payments.csv
│
├── ingest.py # Creates tables + loads CSVs into SQLite
├── run_query.py # Runs SQL JOIN query across 5 tables
│
├── ecommerce.db # SQLite database (auto created after running ingest.py)
│
└── README.md

 Step 1 — Generate Synthetic Data (via Cursor Prompt)
Using Cursor AI, 5 synthetic CSV files were generated:
1. customers.csv— (id, name, email)  
2. products.csv — (id, name, category, price)  
3. orders.csv — (order_id, customer_id, date)  
4. order_items.csv — (order_id, product_id, quantity)  
5. payments.csv— (payment_id, order_id, amount, status)
Each file contains ~20 sample rows of realistic ecommerce data.

Step 2 — Ingest Data Into SQLite Database
Run the following command in Cursor IDE or VS Code terminal:
python ingest.py
The script will:
Create ecommerce.db
Create tables:
customers
products
orders
order_items
payments
Insert all CSV data automatically
Check tables:
sqlite3 ecommerce.db
.tables

Step 3 — SQL JOIN Query (run_query.py)
Run:
python run_query.py
This script runs a multi-table join and prints results.
Step 4 — Push Project to GitHub
git init
git add .
git commit -m "A-SDLC Ecommerce Project"
git branch -M main
git remote add origin git clone https://github.com/rajveerkatoch17/cursor.git
git push -u origin main
Tools Used
Cursor IDE (A-SDLC)
Python 3
SQLite
Git & GitHub

Sample Output
('John Doe', 101, 'Laptop', 1, 55000, 'Success', 55000)
('Aarav Kumar', 102, 'Bluetooth Speaker', 2, 2500, 'Success', 5000)
