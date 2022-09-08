from ast import Num
import asyncio
from dataclasses import dataclass, field
from functools import lru_cache
from typing import  Tuple, Union

import matlab
import matlab.engine
from matlab.engine import MatlabEngine
import numpy as np

Numeric = Union[int, float, list[int], list[float], np.ndarray]


@dataclass(unsafe_hash=True)
class MatlabMath:
    engine: MatlabEngine = field(hash=False)

    async def sin(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        future = self.engine.sin(vector, background=True)
        while not future.done():
            await asyncio.sleep(0)
        result = future.result()
        return matlab_double_to_python(result)
    
    async def cos(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        
        future = self.engine.cos(vector, background=True)
        while not future.done():
            await asyncio.sleep(0)
        result = future.result()
        return matlab_double_to_python(result)

    async def fft(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        future = self.engine.fft(vector, background=True)
        while not future.done():
            await asyncio.sleep(0)
        result = future.result()
        real_result = self.engine.real(result)
        return matlab_double_to_python(real_result)

    async def abs(self, x: Numeric) -> Numeric:
        vector = matlab.double(x)
        future = self.engine.abs(vector, background=True)
        while not future.done():
            await asyncio.sleep(0)
        result = future.result()
        return matlab_double_to_python(result)

    async def power(self, x: Numeric, order: float) -> Numeric:
        vector = matlab.double(x)
        # result = self.engine.power(vector, order)
        # t0 
        future = self.engine.power(vector, order, background=True)
        while not future.done():
            await asyncio.sleep(0)
        result = future.result()
        return matlab_double_to_python(result)

    async def power_spectrum(self, x: Numeric, fs: float) -> Tuple[Numeric, Numeric]:
        n = len(x)
        power = await self.power(await self.abs(await self.fft(x)), fs / n)
        freqs = np.arange(n) * (fs / n)
        return freqs[:n//2], power[:n//2]


def matlab_double_to_python(x: matlab.double) -> Numeric:
    x_array = np.asarray(x).squeeze()
    x_python = x_array.item() if x_array.ndim == 0 else x_array
    return x_python
    

def get_matlab_engine() -> MatlabEngine:
    return matlab.engine.start_matlab()