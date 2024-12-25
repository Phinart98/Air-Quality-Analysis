import numpy as np
from scipy import stats

class StatisticalAnalyzer:
    def __init__(self, data):
        self.data = data
        
    def compute_basic_stats(self, column):
        if self.data is None or column not in self.data.columns:
            return {}
            
        valid_data = self.data[column].dropna()
        if len(valid_data) == 0:
            return {}
            
        stats_dict = {
            'mean': float(valid_data.mean()),
            'median': float(valid_data.median()),
            'std': float(valid_data.std()),
            'min': float(valid_data.min()),
            'max': float(valid_data.max())
        }
        return stats_dict
