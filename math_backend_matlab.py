from ast import Num
from dataclasses import dataclass
from typing import  Tuple, Union

import matlab
import matlab.engine
from matlab.engine import MatlabEngine
import numpy as np

Numeric = Union[int, float, list[int], list[float], np.ndarray]


@dataclass
class MatlabMath:
    engine: MatlabEngine

    def sin(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        sin_x = self.engine.sin(vector)
        return matlab_double_to_python(sin_x)
    
    def cos(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        cos_x = self.engine.cos(vector)
        return matlab_double_to_python(cos_x)

    def fft(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        result = self.engine.fft(vector)
        real_result = self.engine.real(result)
        return matlab_double_to_python(real_result)

    def abs(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        result = self.engine.abs(vector)
        return matlab_double_to_python(result)

    def power(self, x: Numeric, order: float) -> Numeric:
        vector = matlab.double(x)
        result = self.engine.power(vector, order)
        return matlab_double_to_python(result)

    def power_spectrum(self, x: Numeric, fs: float) -> Tuple[Numeric, Numeric]:
        n = len(x)
        power = self.power(self.abs(self.fft(x)), fs / n)
        freqs = np.arange(n) * (fs / n)
        return freqs[:n//2], power[:n//2]


def matlab_double_to_python(x: matlab.double) -> Numeric:
    x_array = np.asarray(x).squeeze()
    x_python = x_array.item() if x_array.ndim == 0 else x_array
    return x_python
    

def get_matlab_engine() -> MatlabEngine:
    return matlab.engine.start_matlab()