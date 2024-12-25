import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd

class SeasonalAnalyzer:
    def __init__(self, data, frequency=24):
        self.data = data
        self.frequency = frequency
        
    def decompose_series(self, column):
        decomposition = seasonal_decompose(
            self.data[column],
            period=self.frequency,
            extrapolate_trend='freq'
        )
        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid
        }
        
    def get_seasonal_strength(self, decomposition):
        var_seasonal = np.var(decomposition['seasonal'])
        var_residual = np.var(decomposition['residual'].dropna())
        strength = var_seasonal / (var_seasonal + var_residual)
        return strength
        
    def extract_seasonal_patterns(self, column):
        hourly_patterns = self.data[column].groupby(self.data.index.hour).mean()
        daily_patterns = self.data[column].groupby(self.data.index.dayofweek).mean()
        monthly_patterns = self.data[column].groupby(self.data.index.month).mean()
        
        return {
            'hourly': hourly_patterns,
            'daily': daily_patterns,
            'monthly': monthly_patterns
        }
