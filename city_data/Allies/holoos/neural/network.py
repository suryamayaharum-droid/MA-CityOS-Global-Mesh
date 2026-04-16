"""HoloOS Neural Network"""
import math
import random
from typing import List

class NeuralNetwork:
    def __init__(self, layer_sizes: List[int]):
        self.weights = []
        self.biases = []
        for i in range(1, len(layer_sizes)):
            self.weights.append([[random.gauss(0, 0.1) for _ in range(layer_sizes[i-1])] for _ in range(layer_sizes[i])])
            self.biases.append([random.gauss(0, 0.1) for _ in range(layer_sizes[i])])
    
    def forward(self, inputs: List[float]) -> List[float]:
        for w, b in zip(self.weights, self.biases):
            outputs = []
            for neuron_w, neuron_b in zip(w, b):
                z = sum(x * y for x, y in zip(inputs, neuron_w)) + neuron_b
                outputs.append(max(0, z))  # ReLU
            inputs = outputs
        return inputs

__all__ = ["NeuralNetwork"]
