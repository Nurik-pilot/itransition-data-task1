import os
import re, json, psycopg2

with open(r"C:\Users\PCHelper\Documents\Itransition\task_1_data\task1_d.json", 'r', encoding='utf-8') as f:
    content = re.sub(r':\s*(\w+)\s*=>', r'"\1":', f.read())
data = json.loads(content)

def convert_price(p):
    if p.startswith('$'): return float(p[1:])
    if p.startswith('€'): return float(p[1:]) * 1.2
    return None

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id TEXT PRIMARY KEY,
        title TEXT, author TEXT, genre TEXT,
        publisher TEXT, year INTEGER, price_usd NUMERIC(10, 4)
    )
''')

for r in data:
    cur.execute('''
        INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id) DO NOTHING
    ''', (str(r['id']), r['title'], r['author'], r['genre'],
          r['publisher'], r['year'], convert_price(r['price'])))
conn.commit()

cur.execute('DROP TABLE IF EXISTS books_summary')
cur.execute('''
    CREATE TABLE books_summary AS
    SELECT year AS publication_year,
           COUNT(*) AS book_count,
           ROUND(AVG(price_usd), 2) AS average_price
    FROM books
    GROUP BY year
    ORDER BY year
''')
conn.commit()

cur.execute('SELECT * FROM books_summary')
print(cur.fetchall())

cur.close()
conn.close()