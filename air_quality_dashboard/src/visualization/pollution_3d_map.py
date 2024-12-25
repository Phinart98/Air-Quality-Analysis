import plotly.graph_objects as go
import numpy as np

class Pollution3DMap:
    def __init__(self, stations_data):
        self.stations_data = stations_data
        
    def create_3d_surface(self, pollutant='pm10'):
        x = self.stations_data.geometry.x.values
        y = self.stations_data.geometry.y.values
        z = self.stations_data[pollutant].values
        
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
        fig.update_layout(
            title=f'{pollutant.upper()} 3D Surface Map',
            scene = dict(
                xaxis_title='Longitude',
                yaxis_title='Latitude',
                zaxis_title=f'{pollutant.upper()} Level'
            )
        )
        return fig
