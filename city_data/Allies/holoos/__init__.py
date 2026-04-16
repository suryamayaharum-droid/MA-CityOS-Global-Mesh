"""HoloOS - Sistema de Super Inteligência Unificada

Versão: 0.8.0 - Python stdlib only
"""

# Core
from core.types import Language, QuantizationFormat, TensorSpec, ModelMetadata, QuantizationConfig
from core.ethical import EthicalCore

# Kernel
from kernel.self_kernel import SelfKernel, Soul
from kernel.consciousness import ConsciousnessCore
from kernel.soul import SoulCore
from kernel.advanced_attention import AdvancedAttention, TransformerBlock

# Security
from security.kernel import SecurityKernel, ThreatLevel

# AI
from ai.hub import AIHub, ModelModality, AIModel

# Memory
from memory.system import MemorySystem

# Tools
from tools.executor import ToolExecutor

# Quantizer
from quantizer.engine import QuantizerEngine

# Compiler
from compiler.transpiler import Transpiler

# Governance
from governance.assembly import Assembly, Role

# Planning
from planning.planner import Planner, ReasoningType

# Communication
from communication.hub import CommunicationHub, EventBus, Protocol
from communication.workflow import WorkflowEngine, Workflow

# Database
from database.manager import DatabaseManager

# Gateway
from gateway.gateway import APIGateway

# Monitoring
from monitoring.system import MonitoringSystem

# Plugins
from plugins.manager import PluginManager

# Config
from config.manager import ConfigManager

# Distributed
from distributed.executor import DistributedExecutor

# Agent
from agent.engine import AgentEngine

# Generator
from generator.code_gen import CodeGenerator

# Quantum
from quantum.engine import QuantumOptimizer

# Neural
from neural.network import NeuralNetwork

__version__ = "0.8.0"

def get_system_status():
    return {
        "name": "HoloOS",
        "version": __version__,
        "modules": 20,
        "languages": 35,
        "quantization_formats": 21,
        "ai_models": 27,
        "tools": 9,
        "security": "active",
        "ethics": "active",
    }

def create_system():
    return {
        "kernel": SelfKernel(),
        "consciousness": ConsciousnessCore(),
        "security": SecurityKernel(),
        "ai": AIHub(),
        "memory": MemorySystem(),
        "tools": ToolExecutor(),
    }

# AI Integrations
from ai.huggingface_integration import HuggingFaceHub
from ai.langchain_integration import LangChainIntegration, Chain, Agent, Memory


# New Integrations
from ai.model_integrations import Gemma4Integration, ClaudeMythosIntegration

