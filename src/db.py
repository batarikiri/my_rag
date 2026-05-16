import psycopg2
from pgvector.psycopg2 import register_vector

class VectorDB:
    def __init__(self, dbname = 'ragdb', user = 'raguser', password = 'ragpass', host = 'localhost', port = 5432):
        print(f"Подключение к POstG: {dbname}@{host}:{port}")
        self.conn = psycopg2.connect(
			database = dbname,
			user = user,
			password = password,
			host = host,
			port = port
		)
        register_vector(self.conn)
        self.cur = self.conn.cursor()
        print("Подключение к БД")


    def search_similar(self, embedding, top_k=5):
        self.cur.execute(
            "SELECT content, source_file FROM documents ORDER BY embedding <=> %s::vector LIMIT %s",
            (embedding.tolist(), top_k)
        )
        return self.cur.fetchall() 
    
    def insert_document(self, content, embedding, source_file):
        self.cur.execute(
            "INSERT INTO documents (content, embedding, source_file) VALUES (%s, %s, %s)",
            (content, embedding.tolist(), source_file)
        )
    
    def commit(self):
        """Фиксация транзакции"""
        self.conn.commit()
    
    def close(self):
        """Закрытие соединения"""
        self.cur.close()
        self.conn.close()