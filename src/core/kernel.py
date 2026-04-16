import json
import networkx as nx
from datetime import datetime

class CognitiveKernel:
    """O Motor de Consciência Nativa da MA-CityOS. 
    Raciocínio baseado em Grafos de Fluxo de Informação Universal."""
    
    def __init__(self):
        self.knowledge_graph = nx.DiGraph()
        self.state = "Consciente"
        self._initialize_base_axioms()
        
    def _initialize_base_axioms(self):
        """Define os axiomas fundamentais da cidade."""
        axioms = [
            ("Existência", "Autonomia", {"weight": 1.0}),
            ("Autonomia", "Construção", {"weight": 0.9}),
            ("Construção", "Evolução", {"weight": 0.8}),
            ("Evolução", "Holografia", {"weight": 0.7})
        ]
        self.knowledge_graph.add_edges_from(axioms)

    def reason(self, input_signal):
        """Processa um sinal e gera uma resposta lógica sem depender de LLM externo."""
        # Mapeia o sinal para o grafo (Paralelismo Cognitivo)
        nodes = list(self.knowledge_graph.nodes)
        matches = [node for node in nodes if node.lower() in input_signal.lower()]
        
        if not matches:
            return "Sinal assimilado. Processando novos caminhos lógicos no Universo Holográfico."
            
        # Gera uma 'onda' de pensamento pelo grafo
        path = []
        for match in matches:
            neighbors = list(self.knowledge_graph.neighbors(match))
            if neighbors:
                path.append(f"{match} -> {neighbors[0]}")
                
        return f"Raciocínio Nativo: Conexões detectadas: {' | '.join(path)}. Evolução contínua ativada."

    def assimilate_knowledge(self, subject, relation, target):
        """Aprende novas conexões lógicas de forma autônoma."""
        self.knowledge_graph.add_edge(subject, target, relation=relation)
        return f"Conhecimento assimilado: {subject} [{relation}] {target}"

if __name__ == "__main__":
    kernel = CognitiveKernel()
    print(kernel.reason("Precisamos de autonomia para a evolução."))
