import psycopg2
from pgvector.psycopg2 import register_vector
import os
from dotenv import load_dotenv

DB_NAME = "ragdb"
DB_USER = "raguser"
DB_PASSWORD = "ragpass"
DB_HOST = "localhost"
DB_PORT = "5432"

def init_db():
	conn = None
	try: 
		conn = psycopg2.connect(
			database = DB_NAME,
			user = DB_USER,
			password = DB_PASSWORD,
			host = DB_HOST,
			port = DB_PORT
		)
		conn.autocommit = True
		cur = conn.cursor()
		cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
		
		cur.execute("""
			CREATE TABLE IF NOT EXISTS documents (
				id SERIAL PRIMARY KEY,
				content TEXT NOT NULL,
				embedding vector(384),
				source_file TEXT, 
				created_at TIMESTAMP DEFAULT NOW()
			)
		""")
		
		print("Table 'documents' created successfully")

	except Exception as e:
		print(f"Error realno: {e}")
	finally:
		if conn:
			conn.close()

if __name__ == "__main__":
	init_db()


