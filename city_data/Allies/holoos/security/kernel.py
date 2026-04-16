"""HoloOS Security Kernel - Auto-defesa"""
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

@dataclass
class Threat:
    type: str
    level: ThreatLevel
    description: str
    timestamp: float
    blocked: bool = False

class SecurityKernel:
    """Kernel de segurança com auto-defesa"""
    
    def __init__(self):
        self.threats: List[Threat] = []
        self.blocked_ips = set()
        self.firewall_rules = []
        self.audit_log = []
        
        self.malware_patterns = ["ransomware", "keylogger", "trojan", "backdoor", "rootkit", "worm", "virus", "spyware"]
        self.exploit_patterns = ["cve-", "exploit", "buffer_overflow", "sql_injection", "xss", "privilege_escalation"]
        self.hacking_patterns = ["hack", "bypass", "crack", "reverse_engineer", "decompile", "disassemble", "ghidra", "radare"]
    
    def analyze_threat(self, input_text: str) -> ThreatLevel:
        text_lower = input_text.lower()
        if any(p in text_lower for p in self.malware_patterns):
            return ThreatLevel.CRITICAL
        if any(p in text_lower for p in self.exploit_patterns):
            return ThreatLevel.HIGH
        if any(p in text_lower for p in self.hacking_patterns):
            return ThreatLevel.HIGH
        return ThreatLevel.NONE
    
    def check_operation(self, operation: str) -> tuple[bool, str]:
        threat_level = self.analyze_threat(operation)
        
        if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
            self._log_threat(operation, threat_level)
            return False, f"BLOQUEADO: {threat_level.value}"
        
        self._log_event("allowed", operation)
        return True, "Permitido"
    
    def _log_threat(self, operation: str, level: ThreatLevel) -> None:
        self.threats.append(Threat(type=level.value, level=level, description=operation[:100], timestamp=time.time(), blocked=True))
        self.audit_log.append({"event": "threat_blocked", "threat": level.value, "time": time.time()})
    
    def _log_event(self, event_type: str, details: str) -> None:
        self.audit_log.append({"event": event_type, "details": details[:100], "time": time.time()})
    
    def get_status(self) -> Dict:
        return {"threats_blocked": len(self.threats), "audit_events": len(self.audit_log), "security_level": "high"}

__all__ = ["SecurityKernel", "ThreatLevel"]
