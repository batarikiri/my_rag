from PyPDF2 import PdfReader
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from embedding import EmbeddingModel
from db import VectorDB

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200 # перекрытие между чанками

def read_pdf(filepath):
	try:
		reader = PdfReader(filepath)
		text = ""
		for page in reader.pages:
			page_text = page.extract_text()
			if page_text:
				text += page_text + " "
		return text.strip()
	except Exception as e:
		print (f" Error of chtenie {filepath}: {e}")
		return None

def chunk_text(text, chunk_size = CHUNK_SIZE, overlap = CHUNK_OVERLAP):
	if not text:
		return []
	chunks = []
	start = 0
	while start < len(text):
		end = min(start + chunk_size, len(text))
		chunk = text[start:end]
		chunks.append(chunk)
		start += chunk_size - overlap
	return chunks

def main():
	embedder = EmbeddingModel()

	db = VectorDB()

	pdf_folder = "data/pdf"
	if not os.path.exists(pdf_folder):
		os.makedirs(pdf_folder)
		print(f"Создана папка {pdf_folder}")
		print("Положите ваши статьи в эту папку и запустие снова скрипт")
		return

	pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
	print(f" Найдено файлов: {len(pdf_files)}")
	
	total_chunks = 0
	for filename in pdf_files:
		filepath = os.path.join(pdf_folder, filename)
		print(f"\n Обработка {filename}")
		text = read_pdf(filepath)
		if  not text:
			print(f"Не удалось извлечь текст из ")
			continue
		print(f" Извлечено символов {len(text)}")
		
		chunks = chunk_text(text)
		print(f"Создано чанков {len(chunks)}")
		
		for i,chunk in enumerate(chunks):
			embedding = embedder.encode(chunk)
			db.insert_document(chunk, embedding, filename)
			
			total_chunks +=1
			if (i+1) % 10 == 0 or i+1 == len(chunks):
				print(f"Созранено {i+1}/{len(chunks)} чанков")
		db.commit()
		print(f" {filename} добавлен в базу")

	print(f"\n Индексировано {total_chunks} чанков из {len(pdf_files)} файлов")
	db.close()
	
if __name__ == "__main__":
	main()









