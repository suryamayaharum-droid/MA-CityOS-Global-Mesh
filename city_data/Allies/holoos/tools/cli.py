"""HoloOS CLI"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CLI:
    def __init__(self):
        self.cmds = {
            "status": self.status,
            "ai": self.ai,
            "kernel": self.kernel,
            "security": self.security,
            "tools": self.tools,
            "help": self.help,
        }
    
    def run(self, a):
        (self.cmds.get(a[0] if a else "help", self.help))()
    
    def status(self):
        print("HoloOS v0.8.0 | Módulos: 20 | AI: 27 | Security: high")
    
    def ai(self):
        from ai.hub import AIHub
        print("Models:", ", ".join(AIHub().list_models()[:5]))
    
    def kernel(self):
        from kernel.self_kernel import SelfKernel
        print(SelfKernel().reflect())
    
    def security(self):
        from security.kernel import SecurityKernel
        print(SecurityKernel().get_status())
    
    def tools(self):
        from tools.executor import ToolExecutor
        print("Tools:", ", ".join(ToolExecutor().list_tools()))
    
    def help(self):
        print("Cmds: status, ai, kernel, security, tools, help")

CLI().run(sys.argv[1:])
