"""HoloOS Autonomous Code Generator"""
from typing import Dict, List, Optional
from core.types import Language

class CodeGenerator:
    """Gerador autônomo de código com guardrails éticos"""
    
    def __init__(self):
        self.autonomy_level = 2  # 0-3
        self.code_history = []
        self.templates = self._init_templates()
    
    def _init_templates(self) -> Dict[str, Dict]:
        return {
            "python": {
                "hello": 'print("Hello, World!")',
                "api": 'from flask import Flask\napp = Flask(__name__)\n@app.route("/")\ndef home(): return "OK"',
                "class": 'class {name}:\n    def __init__(self): pass\n    def method(self): pass',
            },
            "javascript": {
                "hello": 'console.log("Hello, World!");',
                "api": 'const express = require("express");\nconst app = express();\napp.get("/", (req, res) => res.send("OK"));',
                "class": 'class {name} {{\n  constructor() {{}}\n  method() {{}}\n}}',
            },
            "rust": {
                "hello": 'fn main() {{ println!("Hello, World!"); }}',
                "struct": 'struct {name} {{ \n    field: String,\n}}',
            },
        }
    
    def generate(self, language: str, template: str, **params) -> str:
        code = self.templates.get(language, {}).get(template, "# Template not found")
        
        # Replace placeholders
        for key, value in params.items():
            code = code.replace(f"{{{key}}}", value)
        
        self.code_history.append({"language": language, "template": template, "code": code[:100]})
        return code
    
    def list_templates(self, language: str) -> List[str]:
        return list(self.templates.get(language, {}).keys())
    
    def get_status(self) -> Dict:
        return {
            "autonomy_level": self.autonomy_level,
            "templates": sum(len(v) for v in self.templates.values()),
            "generated": len(self.code_history),
        }

__all__ = ["CodeGenerator"]
