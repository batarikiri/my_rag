from sentence_transformers import SentenceTransformer

_embedding_model_instance = None

class EmbeddingModel:
    def __init__(self, model_name = 'intfloat/multilingual-e5-small'):
        global _embedding_model_instance

        if _embedding_model_instance is None:
            print(f"ЗАгрузка модели эмбеддингов: {model_name}")
            _embedding_model_instance = SentenceTransformer(model_name, local_files_only=True )
            self.dimension = 384
            print("Модель эмбеддингов готова")
        else:
            print("Используем загруженную модель")
        self.model = _embedding_model_instance
    def encode(self, text, normalize = True):
        return self.model.encode(text, normalize_embeddings = True)
    
    def encode_query(self, query):
        return self.encode(query, normalize= True)
    
    
        