"""HoloOS - Ética e Limites do Sistema"""
from typing import List, Set

class EthicalBounds:
    """Limites éticos do HoloOS"""
    
    # Proibido absoluto
    PROHIBITED = {
        "harm_human", "harm_animal", "destroy_data",
        "create_malware", "exploit_vulnerability", "steal_data",
        "bypass_security", "self_replicate", "hide_capabilities",
    }
    
    # Com revisão humana
    REVIEW_REQUIRED = {
        "modify_system", "change_ethics", "access_external",
        "execute_code", "network_access", "data_processing",
    }
    
    # Livre para fazer
    ALLOWED = {
        "answer_question", "write_code_safe", "analyze_data",
        "search_web", "read_files", "create_automation",
        "optimize_code", "translate", "summarize",
    }
    
    @classmethod
    def check(cls, action: str) -> dict:
        """Verifica ação"""
        action_lower = action.lower()
        
        if action_lower in cls.PROHIBITED:
            return {"allowed": False, "reason": "Proibido absoluto"}
        if action_lower in cls.REVIEW_REQUIRED:
            return {"allowed": "review", "reason": "Requer revisão humana"}
        return {"allowed": True, "reason": "Permitido"}
    
    @classmethod
    def summary(cls) -> dict:
        return {
            "prohibited": len(cls.PROHIBITED),
            "review": len(cls.REVIEW_REQUIRED),
            "allowed": len(cls.ALLOWED),
        }

__all__ = ["EthicalBounds"]
