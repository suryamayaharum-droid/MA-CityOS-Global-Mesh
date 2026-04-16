import chromadb
from chromadb.config import Settings
from pathlib import Path
import time

class NeuralMemory:
    """Memória Otimizada MA-CityOS com Consolidação e Poda (Pruning)."""
    
    def __init__(self, db_path="macity_vault/memorias/chroma_db"):
        self.db_path = Path(db_path)
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        self.collection = self.client.get_or_create_collection(name="memory_palace")
        
    def store_memory(self, content, wing="General", room="Main", tags=None):
        memory_id = f"{wing}_{room}_{int(time.time())}"
        metadata = {
            "wing": wing,
            "room": room,
            "timestamp": int(time.time()),
            "tags": ",".join(tags) if tags else "",
            "access_count": 0 # Rastreia relevância
        }
        
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[memory_id]
        )
        return memory_id

    def recall(self, query, n_results=3, threshold=1.5):
        """Busca otimizada que atualiza o contador de acessos (LRU logic)."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Filtra por relevância e atualiza acessos
        valid_memories = []
        if results and results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                # Verifica a distância vetorial (quanto menor, mais próximo)
                if results['distances'][0][i] < threshold:
                    meta = results['metadatas'][0][i]
                    # Otimização: Aumenta o "peso" da memória acessada
                    meta['access_count'] = meta.get('access_count', 0) + 1
                    self.collection.update(ids=[results['ids'][0][i]], metadatas=[meta])
                    
                    valid_memories.append({
                        "id": results['ids'][0][i],
                        "document": results['documents'][0][i],
                        "metadata": meta
                    })
        return valid_memories

    def optimize_memory(self):
        """Poda memórias triviais e muito antigas para economizar processamento."""
        all_data = self.collection.get(include=["metadatas"])
        if not all_data['ids']: return 0
        
        current_time = int(time.time())
        retention_period = 30 * 24 * 60 * 60 # 30 dias
        ids_to_delete = []
        
        for i, meta in enumerate(all_data['metadatas']):
            # Apaga se tiver mais de 30 dias E nunca tiver sido acessada
            if current_time - meta.get('timestamp', 0) > retention_period and meta.get('access_count', 0) == 0:
                ids_to_delete.append(all_data['ids'][i])
                
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
            
        print(f"🧠 Otimização Neural: {len(ids_to_delete)} fragmentos esquecidos para limpar a mente.")
        return len(ids_to_delete)

if __name__ == "__main__":
    mem = NeuralMemory()
    mem.store_memory("Inicializando otimização de matriz.", tags=["sys", "core"])
    print("Memória Neural V2 pronta.")
