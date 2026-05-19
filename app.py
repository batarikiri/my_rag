import sys
import os
import gradio as gr


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from embedding import EmbeddingModel
from db import VectorDB
from ollama_client import OllamaClient


def get_rag_answer(question):

    embedder = EmbeddingModel()
    db = VectorDB()
    llm = OllamaClient()
    
    if not question or not question.strip():
        yield "Вопрос не может быть пустым"
        return

    q_embedding = embedder.encode_query(question)
    results = db.search_similar(q_embedding, top_k=3)
    
    if not results:
        yield "Ничего не найдено в базе"
        return
    

    context = "\n\n---\n\n".join([r[0] for r in results])
    

    prompt = f"Контекст: {context}\nВопрос: {question}\nОтвет:"
    
    full_answer = ""
    for chunk in llm.generate_stream(prompt):
        full_answer += chunk
        yield full_answer

def chat_with_rag(message, history):
    """Обёртка для Gradio"""
    for chunk in get_rag_answer(message):
        yield chunk


demo = gr.ChatInterface(
    fn=chat_with_rag,
    title="RAG Assistant",
    description="Задайте вопрос по вашим научным статьям"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7862)
