import socket
import json
import time

nodes = ["172.17.0.3", "172.17.0.4", "172.17.0.5", "172.17.0.6", "172.17.0.7"]
port = 8888

def boost_signal():
    print("⚡ MESH BOOSTER: Amplificando sinal da malha...")
    for target in nodes:
        for peer in nodes:
            if target != peer:
                try:
                    # Tenta enviar um sinal de pulso para cada nó
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((target, port))
                    msg = json.dumps({"sender": "BOOSTER", "action": "SYNC_PEER", "peer": peer})
                    s.send(msg.encode())
                    s.close()
                    print(f"   ✅ Sinal linkado: {target} -> {peer}")
                except:
                    print(f"   ❌ Falha no link: {target} -> {peer}")

if __name__ == "__main__":
    boost_signal()
