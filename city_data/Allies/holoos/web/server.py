"""HoloOS Web API Server"""
import json
import http.server
import socketserver
from urllib.parse import urlparse
PORT = 5000

import sys
sys.path.insert(0, '.')
from kernel.self_kernel import SelfKernel
from ai.hub import AIHub
from memory.system import MemorySystem
from tools.executor import ToolExecutor
from security.kernel import SecurityKernel

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path).path
        
        if p == '/':
            self.send_json({"name": "HoloOS", "version": "0.8.0", "status": "online"})
        
        elif p == '/status':
            k = SelfKernel()
            ai = AIHub()
            m = MemorySystem()
            t = ToolExecutor()
            s = SecurityKernel()
            
            self.send_json({
                "kernel": k.get_status(),
                "ai": ai.get_status(),
                "memory": m.get_status(),
                "tools": len(t.tools),
                "security": s.get_status(),
            })
        
        elif p == '/kernel/think':
            k = SelfKernel()
            result = k.think("API request")
            self.send_json({"response": result})
        
        elif p == '/ai/chat':
            ai = AIHub()
            result = ai.chat("Hello from API")
            self.send_json({"response": result})
        
        elif p == '/security/check':
            s = SecurityKernel()
            allowed, reason = s.check_operation("help")
            self.send_json({"allowed": allowed, "reason": reason})
        
        else:
            self.send_error(404)
    
    def send_json(self, d):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())
    
    def log_message(self, format, *args):
        pass  # Suppress logging

print(f"🚀 HoloOS API: http://localhost:{PORT}")
print("Endpoints: /, /status, /kernel/think, /ai/chat, /security/check")
socketserver.TCPServer(("", PORT), Handler).serve_forever()
