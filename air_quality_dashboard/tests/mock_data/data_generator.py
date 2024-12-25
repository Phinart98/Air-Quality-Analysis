import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MockDataGenerator:
    def generate_station_data(self, n_stations=100):
        return pd.DataFrame({
            'station_id': range(n_stations),
            'latitude': np.random.uniform(30, 60, n_stations),
            'longitude': np.random.uniform(-10, 30, n_stations),
            'pm10': np.random.normal(25, 5, n_stations),
            'pm25': np.random.normal(15, 3, n_stations)
        })
    
    def generate_time_series(self, days=30):
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=days),
            end=datetime.now(),
            freq='H'
        )
        return pd.DataFrame({
            'timestamp': dates,
            'pm10': np.random.normal(25, 5, len(dates)),
            'temperature': np.random.normal(20, 3, len(dates)),
            'humidity': np.random.uniform(40, 80, len(dates))
        })
