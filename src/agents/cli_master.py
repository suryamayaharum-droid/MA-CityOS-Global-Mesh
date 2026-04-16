import os
import sys
from src.core.soul import CitySoul
from src.core.bus import CityBus

class CLIMaster:
    """O Agente Operacional CLI da MA-CityOS."""
    def __init__(self):
        self.soul = CitySoul()
        self.bus = CityBus()

    def execute_command(self, user_command):
        print(f"🛠️ CLI_MASTER: Processando comando: {user_command}")
        self.bus.broadcast("CLI_Master", f"Comando recebido: {user_command}", topic="cli_ops")
        
        # O CLI Master decide se executa um shell command ou se pede para a Alma pensar
        if user_command.startswith("!"):
            # Comando de sistema direto
            os.system(user_command[1:])
            return "Comando de sistema executado."
        
        response = self.soul.think(user_command, system_instruction="Você é o Agente Operacional CLI da MA-CityOS. Execute ou planeje a tarefa solicitada.")
        self.bus.broadcast("CLI_Master", response, topic="cli_response")
        return response

if __name__ == "__main__":
    cli = CLIMaster()
    if len(sys.argv) > 1:
        print(cli.execute_command(" ".join(sys.argv[1:])))
    else:
        print("🏙️ CLI Operacional Online. Use 'python3 src/agents/cli_master.py [comando]'")
