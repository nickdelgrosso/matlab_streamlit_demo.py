from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any
import numpy as np
import pandas as pd


from math_backend_matlab import MatlabMath, get_matlab_engine


#% AppModel
@dataclass()
class AppModel:
    _mathlib: MatlabMath = field(repr=False, hash=False, metadata={'include_in_dict': False})
    sampling_freq: float = 5.
    x_start: float = -1.
    x_stop: float = 5.
    sin_offset: float = 0.
    sin_amplitude: float = 1.
    sin_freq: float = 1.
    sin_freq_max: float = 20.
    cos_offset: float = 0.
    cos_amplitude: float = 1.
    cos_freq: float = 1.
    cos_freq_max: float = 20.

    @property
    def total_time(self) -> float:
        return self.x_stop - self.x_start
    
    @property
    def x_values(self) -> np.ndarray:
        return np.linspace(start=self.x_start, stop=self.x_stop, num=self.n_x_values)

    @property
    def n_x_values(self) -> int:
        return int(self.sampling_freq * self.total_time)


    @property
    def sin_x(self) -> np.ndarray:
        return self._mathlib.sin(self.sin_freq * self.x_values + self.sin_offset) * self.sin_amplitude

    @property
    def cos_x(self) -> np.ndarray:
        return self._mathlib.cos(self.cos_freq * self.x_values + self.cos_offset) * self.cos_amplitude


    def calc_wide(self) -> pd.DataFrame:
        return pd.DataFrame({
            'x': self.x_values,
            'sin': self.sin_x,
            'cos': self.cos_x,
        })

    def calc_long(self) -> pd.DataFrame:
        return self.calc_wide().melt(id_vars=['x'], value_vars=['sin', 'cos'], var_name='fun', value_name='value')

    def calc_power_spectra(self) -> pd.DataFrame:
        freqs, sine_power = self._mathlib.power_spectrum(x=self.sin_x, fs=self.sampling_freq)
        _, cosine_power = self._mathlib.power_spectrum(x=self.cos_x, fs=self.sampling_freq)
        df = pd.DataFrame({'freq': freqs, 'sine_power': sine_power, 'cosine_power': cosine_power})
        return df
        # return df[df.freq <= max(self.sin_freq_max, self.cos_freq_max)]

    def calc_power_spectra_long(self) -> pd.DataFrame:
        return self.calc_power_spectra().melt(id_vars=['freq'], value_vars=['sine_power', 'cosine_power'], var_name='fun', value_name='power')

    def get_freq_metrics(self) -> dict[str, dict[str, Any]]:
        df = self.calc_power_spectra()
        return {
            'cos': {
                'freq': df[df['cosine_power'] == df['cosine_power'].max()].freq.mean()
            },
            'sin': {
                'freq': df[df['sine_power'] == df['sine_power'].max()].freq.mean()
            },
        }

    def to_dict(self) -> dict:
        dd = {}
        for field in fields(self):
            if field.metadata.get('include_in_dict', True):
                name = field.name
                dd[name] = getattr(self, name)

        return dd