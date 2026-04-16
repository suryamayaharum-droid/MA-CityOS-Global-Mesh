import chromadb
from chromadb.config import Settings
from pathlib import Path
import time

class NeuralMemory:
    def __init__(self, db_path="macity_vault/memorias/chroma_db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        try:
            self.collection = self.client.get_or_create_collection(name="memory_palace")
        except Exception as e:
            print(f"⚠️ MEMORY: Erro ao acessar coleção. Recriando... {e}")
            self.collection = self.client.create_collection(name=f"memory_palace_{int(time.time())}")
        
    def store_memory(self, content, wing="General", room="Main", Hall="Facts", tags=None):
        memory_id = f"{wing}_{room}_{int(time.time())}"
        metadata = {"wing": wing, "room": room, "hall": Hall, "tags": ",".join(tags) if tags else ""}
        try:
            self.collection.add(documents=[content], metadatas=[metadata], ids=[memory_id])
            return memory_id
        except Exception as e:
            print(f"❌ MEMORY_ERROR: {e}")
            return None

    def recall(self, query, n_results=3):
        return self.collection.query(query_texts=[query], n_results=n_results)
