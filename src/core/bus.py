import json
import time
from datetime import datetime
from pathlib import Path

class CityBus:
    """O Barramento de Comunicação da MA-CityOS."""
    
    def __init__(self, vault_path="macity_vault"):
        self.vault_path = Path(vault_path)
        self.log_path = self.vault_path / "Logs"
        self.log_path.mkdir(exist_ok=True)
        
    def broadcast(self, sender, message, topic="general"):
        """Envia uma mensagem para a assembleia."""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "topic": topic,
            "content": message
        }
        
        # Log no Obsidian para visibilidade humana
        log_file = self.log_path / f"interactions_{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(log_file, "a") as f:
            f.write(f"### [{payload['timestamp']}] {sender} -> #{topic}\n")
            f.write(f"{message}\n\n---\n")
            
        print(f"📡 [BUS] {sender}: {message[:50]}...")
        return payload

if __name__ == "__main__":
    bus = CityBus()
    bus.broadcast("Sistema", "As ruas da cidade foram pavimentadas. Barramento online.", topic="syslog")
