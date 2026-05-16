import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from embedding import EmbeddingModel
from db import VectorDB
from ollama_client import OllamaClient

def main():
	print("RAG ассистент...")
	embedder = EmbeddingModel()
	db = VectorDB()
	llm = OllamaClient()

	print("\n" + "="*50)
	question = input("Ваш вопрос: ").strip()

	if not question:
		print("Вопрос не может быть пустым")
		return

	print("\n Поиск релевантных фрагментов....")

	q_embedding = embedder.encode_query(question)
	results = db.search_similar(q_embedding, top_k = 5)

	if not results:
		print("Ничего не найдено в базе")
		return
	

	print(f"\n НАйдено {len(results)} релевантных фрагментов:")
	for i, (_, source) in enumerate(results):
		print(f"  {i+1}. {source}")
		context = "\n\n---\n\n".join([r[0] for r in results])

	prompt = f"Контекст: {context}\nВопрос: {question}\nОтвет:"
	
	print("\n генерация ответа...")
	#answer = llm.generate_with_context(question, context)

	print("ОТВЕТ:")
	full_answer = ""
	for chunk in llm.generate_stream(prompt):
		print(chunk, end="",flush = True)
		full_answer+=chunk

	#print(answer)

if __name__ == "__main__":
	main()
