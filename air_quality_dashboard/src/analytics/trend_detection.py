from scipy import stats
import numpy as np

class TrendDetector:
    def detect_trend(self, data):
        x = np.arange(len(data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
        return {
            'slope': slope,
            'p_value': p_value,
            'r_squared': r_value**2
        }
