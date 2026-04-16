"""HoloOS Quantizer Engine"""
from core.types import QuantizationFormat, TensorSpec

class QuantizerEngine:
    BACKENDS = ["gguf", "gptq", "awq", "bnb", "fp8", "holo"]
    
    def quantize(self, tensor: TensorSpec, bits: int, fmt: str) -> TensorSpec:
        tensor.quantized_dtype = f"{fmt}_q{bits}"
        return tensor
    
    def supported_formats(self) -> list:
        return [f.value for f in QuantizationFormat]

__all__ = ["QuantizerEngine"]
