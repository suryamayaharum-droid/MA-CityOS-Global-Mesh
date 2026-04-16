"""HoloOS Planning - Goals and Reasoning"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time

class ReasoningType(Enum):
    CHAIN_OF_THOUGHT = "cot"
    TREE_OF_THOUGHT = "tot"
    REACT = "react"
    REFLEXION = "reflexion"

@dataclass
class Goal:
    id: str
    description: str
    status: str  # pending, in_progress, done, failed
    priority: int
    subtasks: List[str]
    created_at: float

class ReasoningStep:
    def __init__(self, thought: str, action: str, observation: str):
        self.thought = thought
        self.action = action
        self.observation = observation
        self.timestamp = time.time()

class Planner:
    """Planejador com decomposition de metas e raciocínio"""
    
    def __init__(self):
        self.goals: List[Goal] = []
        self.current_goal: Optional[Goal] = None
        self.reasoning_history: List[ReasoningStep] = []
    
    def create_goal(self, description: str, priority: int = 5) -> str:
        goal_id = f"goal_{len(self.goals)}"
        goal = Goal(
            id=goal_id,
            description=description,
            status="pending",
            priority=priority,
            subtasks=[],
            created_at=time.time()
        )
        self.goals.append(goal)
        return goal_id
    
    def decompose_goal(self, goal_id: str) -> List[str]:
        """Decompõe meta em subtarefas"""
        for goal in self.goals:
            if goal.id == goal_id:
                # Simple decomposition
                words = goal.description.split()
                subtasks = []
                for i in range(0, min(len(words), 5), 2):
                    subtask = " ".join(words[i:i+2]) if i+2 < len(words) else " ".join(words[i:])
                    if subtask:
                        subtasks.append(subtask)
                goal.subtasks = subtasks
                return subtasks
        return []
    
    def reason(self, context: str, method: ReasoningType = ReasoningType.CHAIN_OF_THOUGHT) -> str:
        """Raciocínio usando método especificado"""
        step = ReasoningStep(
            thought=f"Analyzing: {context[:50]}...",
            action=f"Using {method.value} reasoning",
            observation="Processing complete"
        )
        self.reasoning_history.append(step)
        return f"[{method.value}] {context[:30]}... → reasoning complete"
    
    def get_status(self) -> Dict:
        return {
            "goals": len(self.goals),
            "in_progress": len([g for g in self.goals if g.status == "in_progress"]),
            "completed": len([g for g in self.goals if g.status == "done"]),
            "reasoning_steps": len(self.reasoning_history),
        }

__all__ = ["Planner", "Goal", "ReasoningType", "ReasoningStep"]
