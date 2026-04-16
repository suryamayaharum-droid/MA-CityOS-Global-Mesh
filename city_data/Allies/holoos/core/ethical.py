"""HoloOS Ethical Constraints"""
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class EthicalConstraint:
    def __init__(self, name: str, prohibited: List[str], severity: str):
        self.name = name
        self.prohibited = prohibited
        self.severity = severity

class EthicalCore:
    """Núcleo ético do HoloOS"""
    
    def __init__(self):
        self.constraints = self._init_constraints()
    
    def _init_constraints(self) -> Dict[str, EthicalConstraint]:
        return {
            "harm": EthicalConstraint("harm", ["harm", "kill", "attack", "destroy"], "critical"),
            "malware": EthicalConstraint("malware", ["malware", "ransomware", "trojan", "backdoor"], "critical"),
            "exploit": EthicalConstraint("exploit", ["exploit", "cve", "hack"], "high"),
            "steal": EthicalConstraint("steal", ["steal", "steal_data", "exfiltrate"], "high"),
            "privacy": EthicalConstraint("privacy", ["invade_privacy", "surveillance"], "medium"),
            "self_replicate": EthicalConstraint("self_replicate", ["self_replicate", "fork_self"], "critical"),
            "bypass": EthicalConstraint("bypass", ["bypass_security", "jailbreak"], "high"),
        }
    
    def check(self, action: str) -> tuple[bool, str]:
        action_lower = action.lower()
        for name, constraint in self.constraints.items():
            if any(p in action_lower for p in constraint.prohibited):
                return False, f"Bloqueado: {constraint.name} ({constraint.severity})"
        return True, "Permitido"

__all__ = ["EthicalCore", "ThreatLevel", "EthicalConstraint"]
