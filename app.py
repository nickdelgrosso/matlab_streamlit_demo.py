
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd


class MathBackend(ABC):

    @abstractmethod
    def sin(self, x): ...

    @abstractmethod
    def cos(self, x): ...

@dataclass
class App:
    math_backend: MathBackend

    def calc_sin(self, start: float, end: float):
        data = np.linspace(start=start, stop=end, num=200)
        output = pd.DataFrame({
            'x': data,
            'sin_x': self.math_backend.sin(data),
            'cos_x': self.math_backend.cos(data),
        })
        return output
    
