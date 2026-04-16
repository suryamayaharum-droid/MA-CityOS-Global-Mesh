import socket
import threading
import json
import time

class P2PNode:
    """Nó da Malha: Conecta esta instância a outros terminais reais."""
    
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.peers = set() # Lista de IP:Porta de outros bairros
        self.node_id = f"District-{int(time.time())}"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"🌐 P2P BUS: Ouvindo conexões em {self.host}:{self.port} (Node: {self.node_id})")
            
            # Roda o servidor em uma thread separada para não travar o kernel
            threading.Thread(target=self._accept_connections, daemon=True).start()
        except Exception as e:
            print(f"⚠️ Erro ao iniciar servidor P2P: {e}")

    def _accept_connections(self):
        while True:
            try:
                client, address = self.server_socket.accept()
                print(f"🤝 P2P: Nova conexão de vizinho -> {address}")
                threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()
            except: pass

    def _handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data: break
                msg = json.loads(data)
                print(f"📬 P2P Mensagem Recebida: {msg.get('action')} de {msg.get('sender')}")
            except: break
        client_socket.close()

    def connect_to_peer(self, peer_ip, peer_port):
        """Conecta proativamente a outro bairro da malha."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer_ip, peer_port))
            msg = json.dumps({"sender": self.node_id, "action": "HANDSHAKE"})
            s.send(msg.encode('utf-8'))
            self.peers.add(f"{peer_ip}:{peer_port}")
            print(f"✅ P2P: Conectado com sucesso ao Bairro {peer_ip}:{peer_port}")
            s.close()
        except Exception as e:
            print(f"❌ P2P: Falha ao conectar ao bairro {peer_ip}: {e}")

if __name__ == "__main__":
    node = P2PNode()
    node.start_server()
    # Mantém o script rodando para teste
    while True: time.sleep(1)
