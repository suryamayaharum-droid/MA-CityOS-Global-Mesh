"""HoloOS Transpiler"""
from core.types import Language

class Transpiler:
    def __init__(self):
        self.languages = [l.value for l in Language]
    
    def transpile(self, code: str, from_lang: str, to_lang: str) -> str:
        return f"# From {from_lang} to {to_lang}\n{code}"
    
    def list_languages(self) -> list:
        return self.languages

__all__ = ["Transpiler"]
