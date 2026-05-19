import requests
import json

class OllamaClient:
    def __init__(self, url = "http://localhost:11434/api/generate", model = "llama3.2:3b"):
        self.url = url
        self.model = model
        print(f"Ollama клиент готов. Модель {model}")
    def generate(self, prompt, temperature = 0.1):
        payload = {
		    "model": self.model,
		    "prompt": prompt, 
		    "stream": True,
            "options": { 
                "num_ctx": 2048,
                "num_predict": 256,
                "temperature": temperature,
                "num_thread": 4
                }
	    }
	
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "Нет ответа от модели")
        except Exception as e:
            return f"Ошибка при вызове Ollama: {e}" 

    def generate_stream(self, prompt, temperature = 0.1):
        payload = {
		    "model": self.model,
		    "prompt": prompt, 
		    "stream": True,
            "options": { 
                "num_ctx": 4096,
                "num_predict": 512,
                "temperature": temperature,
                "num_thread": 4
                }
	    }

        try:
            response = requests.post(self.url, json=payload, stream=True)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        if token: 
                            full_response += token
                            yield token
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            yield f"Ошибка при вызове Ollama: {e}" 

    def generate_with_context(self, question, context, system_prompt = None):
        if system_prompt is None:
            system_prompt = """Ты — ассистент для анализа научных статей. 
Отвечай на вопрос, используя ТОЛЬКО предоставленный контекст.
Если ответа нет в контексте, скажи: "В статьях нет информации на этот вопрос"."""

        prompt = f"""{system_prompt}

КОНТЕКСТ: 
{context}

ВОПРОС: {question}

ОТВЕТ:""" 
        return self.generate(prompt)
