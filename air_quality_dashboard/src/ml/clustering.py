from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

class StationClusterer:
    def __init__(self, n_clusters=5):
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        
    def prepare_data(self, stations_data):
        features = np.column_stack([
            stations_data.geometry.x,
            stations_data.geometry.y,
            stations_data['pm10']
        ])
        return self.scaler.fit_transform(features)
        
    def cluster_stations(self, stations_data):
        features = self.prepare_data(stations_data)
        clusters = self.model.fit_predict(features)
        return clusters
        
    def get_cluster_centers(self):
        centers = self.scaler.inverse_transform(self.model.cluster_centers_)
        return centers
