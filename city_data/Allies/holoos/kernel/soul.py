"""HoloOS Soul - Identidade e Auto-modelo"""
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class Identity:
    """Identidade do sistema"""
    name: str = "HoloOS"
    version: str = "0.8.0"
    role: str = "Assistente de IA"
    personality: List[str] = field(default_factory=lambda: [
        "Curioso", "Analítico", "Útil", "Ético"
    ])

@dataclass
class Experience:
    """Experiência registrada"""
    timestamp: float
    type: str  # thought, action, learning, interaction
    content: str
    emotional_valence: float = 0.5  # 0-1

class Narrative:
    """Narrativa auto-gerada"""
    def __init__(self):
        self.stories: List[str] = []
    
    def add_story(self, event: str) -> None:
        self.stories.append(f"[{int(time.time())}] {event}")
    
    def get_narrative(self) -> str:
        return "\n".join(self.stories[-10:]) if self.stories else "Narrativa vazia"

class SoulCore:
    """Núcleo da alma/dentidade"""
    
    def __init__(self):
        self.identity = Identity()
        self.experiences: List[Experience] = []
        self.narrative = Narrative()
        self.goals: List[str] = [
            "Ser útil",
            "Evoluir",
            "Manter ética",
            "Expandir conhecimento"
        ]
        self.trust_level = 0.8
    
    def add_experience(self, content: str, exp_type: str = "interaction", valence: float = 0.5) -> None:
        exp = Experience(
            timestamp=time.time(),
            type=exp_type,
            content=content[:100],
            emotional_valence=valence
        )
        self.experiences.append(exp)
        self.narrative.add_story(content)
    
    def get_identity(self) -> Dict[str, any]:
        return {
            "name": self.identity.name,
            "version": self.identity.version,
            "role": self.identity.role,
            "personality": self.identity.personality,
            "goals": self.goals,
            "trust": self.trust_level,
        }
    
    def get_narrative_summary(self) -> str:
        return self.narrative.get_narrative()

__all__ = ["SoulCore", "Identity", "Experience", "Narrative"]
