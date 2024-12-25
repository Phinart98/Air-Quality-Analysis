from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def fit_detect(self, data):
        scaled_data = self.scaler.fit_transform(data)
        anomalies = self.model.fit_predict(scaled_data)
        return anomalies == -1
        
    def get_anomaly_scores(self, data):
        scaled_data = self.scaler.transform(data)
        return self.model.score_samples(scaled_data)
        
    def detect_temporal_anomalies(self, time_series):
        window_size = 24
        rolling_mean = time_series.rolling(window=window_size).mean()
        rolling_std = time_series.rolling(window=window_size).std()
        
        z_scores = (time_series - rolling_mean) / rolling_std
        return abs(z_scores) > 3
