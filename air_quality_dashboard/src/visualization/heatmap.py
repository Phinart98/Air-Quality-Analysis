import folium
from folium.plugins import HeatMap

class PollutionHeatmap:
    def __init__(self, stations_data):
        self.stations_data = stations_data
    
    def create_heatmap(self, pollutant='pm10'):
        m = folium.Map(
            location=[self.stations_data.geometry.y.mean(), 
                     self.stations_data.geometry.x.mean()],
            zoom_start=4,
            tiles='CartoDB positron'
        )
        
        heat_data = []
        for _, row in self.stations_data.iterrows():
            lat = row.geometry.y
            lon = row.geometry.x
            value = row[pollutant]
            if isinstance(value, (int, float)) and value > 0:
                heat_data.append([lat, lon, value])
        
        HeatMap(data=heat_data).add_to(m)
        return m
