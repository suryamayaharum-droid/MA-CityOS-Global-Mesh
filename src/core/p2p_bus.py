import os
import json
import time
from datetime import datetime
from pathlib import Path

class LocalP2PBus:
    """Barramento P2P Local para Paralelismo Cognitivo sem nuvem."""
    def __init__(self, mesh_path="macity_vault/mesh"):
        self.mesh_path = Path(mesh_path)
        self.mesh_path.mkdir(exist_ok=True)
        self.instance_id = os.uname().nodename + "_" + str(os.getpid())

    def emit_signal(self, topic, content):
        """Emite um sinal para outras instâncias lerem."""
        signal = {
            "timestamp": datetime.now().isoformat(),
            "sender": self.instance_id,
            "topic": topic,
            "content": content
        }
        signal_file = self.mesh_path / f"signal_{self.instance_id}_{int(time.time())}.json"
        with open(signal_file, "w") as f:
            json.dump(signal, f)
        return signal

    def scan_signals(self):
        """Lê sinais de outras instâncias."""
        signals = []
        for file in self.mesh_path.glob("*.json"):
            try:
                with open(file, "r") as f:
                    sig = json.load(f)
                    if sig["sender"] != self.instance_id:
                        signals.append(sig)
            except:
                pass
        return signals

if __name__ == "__main__":
    p2p = LocalP2PBus()
    p2p.emit_signal("handshake", "Instância local ativa e aguardando peer.")
    print("📡 P2P_BUS: Sinal emitido na malha local.")
