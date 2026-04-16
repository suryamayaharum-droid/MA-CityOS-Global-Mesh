import sys
import os
from src.agents.mayor import MayorAgent

def main():
    print("--- 🏙️ MA-CityOS: SISTEMA OPERACIONAL META AGENTES INICIALIZADO ---")
    print("Siga para o diretório 'macity_vault' para ver os logs no Obsidian.")
    print("-" * 60)
    
    mayor = MayorAgent(project_id="project-10711253-64de-4044-bb9")
    
    if len(sys.argv) > 1:
        # Se houver argumentos, processa como uma ordem única
        order = " ".join(sys.argv[1:])
    else:
        # Modo interativo padrão
        order = "Inicie a governança da cidade e reporte o status atual dos distritos de memória e comunicação."
        
    print(f"Comando recebido: {order}")
    response = mayor.process_order(order)
    
    print("\n--- 📜 RESPOSTA DO PREFEITO ---")
    print(response)
    print("-" * 60)

if __name__ == "__main__":
    main()
