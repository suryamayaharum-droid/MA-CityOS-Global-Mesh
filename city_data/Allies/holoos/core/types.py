"""HoloOS Core Types - All Programming Languages"""
from enum import Enum
from dataclasses import dataclass
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
class Language(Enum):
    # Systems
    C = "c"
    CPP = "cpp"
    RUST = "rust"
    GO = "go"
    ZIG = "zig"
    NIM = "nim"
    FORTRAN = "fortran"
    COBOL = "cobol"
    # Web
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    HTML = "html"
    CSS = "css"
    PHP = "php"
    RUBY = "ruby"
    DART = "dart"
    # Mobile
    SWIFT = "swift"
    
    # Enterprise
    JAVA = "java"
    CSHARP = "csharp"
    SCALA = "scala"
    # Script
    PYTHON = "python"
    PERL = "perl"
    LUA = "lua"
    BASH = "bash"
    POWERSHELL = "powershell"
    # Functional
    HASKELL = "haskell"
    ELIXIR = "elixir"
    CLOJURE = "clojure"
    # Data
    R = "r"
    MATLAB = "matlab"
    JULIA = "julia"
    SQL = "sql"
    # Other
    ASSEMBLY = "asm"
    LISP = "lisp"
    PROLOG = "prolog"
    GROOVY = "groovy"
    
LANGUAGE_EXTENSIONS = {
    "c": ".c", "cpp": ".cpp", "rust": ".rs", "go": ".go",
    "javascript": ".js", "typescript": ".ts", "python": ".py",
    "java": ".java", "csharp": ".cs", "ruby": ".rb",
    "php": ".php", "swift": ".swift", "kotlin": ".kt",
    "html": ".html", "css": ".css", "sql": ".sql",
    "bash": ".sh", "powershell": ".ps1", "lua": ".lua",
    "haskell": ".hs", "elixir": ".ex", "scala": ".scala",
    "r": ".r", "matlab": ".m", "julia": ".jl",
}
class QuantizationFormat(Enum):
    GGUF_Q2_K = "gguf_q2_k"
    GGUF_Q3_K_S = "gguf_q3_k_s"
    GGUF_Q4_0 = "gguf_q4_0"
    GGUF_Q4_K_M = "gguf_q4_k_m"
    GGUF_Q5_K_M = "gguf_q5_k_m"
    GGUF_Q6_K = "gguf_q6_k"
    GGUF_Q8_0 = "gguf_q8_0"
    GPTQ_INT4 = "gptq_int4"
    GPTQ_INT3 = "gptq_int3"
    GPTQ_INT8 = "gptq_int8"
    AWQ_INT4 = "awq_int4"
    BNB_INT4 = "bnb_int4"
    BNB_INT4_DQ = "bnb_int4_dq"
    BNB_INT8 = "bnb_int8"
    FP8_E4M3 = "fp8_e4m3"
    FP8_E5M2 = "fp8_e5m2"
    ONNX_INT4 = "onnx_int4"
    ONNX_INT8 = "onnx_int8"
    HOLO_VQ = "holo_vq"
    HOLO_RVQ = "holo_rvq"
    HOLO_HQ8 = "holo_hq8"
@dataclass
class TensorSpec:
    name: str
    shape: tuple
    dtype: str
    quantized_dtype: Optional[str] = None
    scale: Optional[float] = None
@dataclass
class ModelMetadata:
    name: str
    architecture: str
    num_parameters: int
    layers: int
@dataclass
class QuantizationConfig:
    format: QuantizationFormat
    bits: int
    group_size: int = 128
__all__ = ["Language", "LANGUAGE_EXTENSIONS", "QuantizationFormat", "TensorSpec", "ModelMetadata", "QuantizationConfig"]
