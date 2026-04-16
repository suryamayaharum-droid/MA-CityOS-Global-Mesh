"""HoloOS Governance Assembly - Meta-governança"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time

class Role(Enum):
    WORKER = "worker"
    COORDINATOR = "coordinator"
    LEGISLATOR = "legislator"
    JUDICIARY = "judiciary"
    EXECUTIVE = "executive"

@dataclass
class Proposal:
    id: str
    title: str
    description: str
    proposer: Role
    votes_for: int = 0
    votes_against: int = 0
    status: str = "pending"
    timestamp: float = 0
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()

class AssemblyMember:
    def __init__(self, role: Role, name: str):
        self.role = role
        self.name = name
        self.votes = 0
    
    def vote(self, proposal: Proposal, approve: bool) -> None:
        if approve:
            proposal.votes_for += 1
        else:
            proposal.votes_against += 1
        self.votes += 1

class Assembly:
    """Assembleia de meta-governança"""
    
    def __init__(self):
        self.members = {
            Role.WORKER: AssemblyMember(Role.WORKER, "Worker-1"),
            Role.COORDINATOR: AssemblyMember(Role.COORDINATOR, "Coordinator-1"),
            Role.LEGISLATOR: AssemblyMember(Role.LEGISLATOR, "Legislator-1"),
            Role.JUDICIARY: AssemblyMember(Role.JUDICIARY, "Judiciary-1"),
            Role.EXECUTIVE: AssemblyMember(Role.EXECUTIVE, "Executive-1"),
        }
        self.proposals: List[Proposal] = []
        self.passed_laws: List[str] = []
    
    def create_proposal(self, title: str, description: str, proposer: Role) -> str:
        prop_id = f"prop_{len(self.proposals) + 1}"
        proposal = Proposal(id=prop_id, title=title, description=description, proposer=proposer)
        self.proposals.append(proposal)
        return prop_id
    
    def vote(self, prop_id: str, role: Role, approve: bool) -> bool:
        for prop in self.proposals:
            if prop.id == prop_id:
                self.members[role].vote(prop, approve)
                if prop.votes_for >= 3:
                    prop.status = "passed"
                    self.passed_laws.append(prop.title)
                    return True
        return False
    
    def get_status(self) -> Dict:
        return {
            "members": len(self.members),
            "proposals": len(self.proposals),
            "passed_laws": len(self.passed_laws),
        }

__all__ = ["Assembly", "Role", "Proposal"]
