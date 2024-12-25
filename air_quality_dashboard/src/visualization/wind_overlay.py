import plotly.graph_objects as go
import numpy as np

class WindOverlay:
    def __init__(self, stations_data):
        self.stations_data = stations_data
    
    def create_wind_map(self, wind_speed, wind_direction):
        fig = go.Figure()
        
        # Add station markers
        fig.add_trace(go.Scattergeo(
            lon=self.stations_data.geometry.x,
            lat=self.stations_data.geometry.y,
            mode='markers',
            marker=dict(size=8),
            name='Stations'
        ))
        
        # Add wind arrows
        fig.add_trace(go.Scattergeo(
            lon=self.stations_data.geometry.x,
            lat=self.stations_data.geometry.y,
            mode='lines',
            line=dict(width=2, color='red'),
            name='Wind Direction'
        ))
        
        fig.update_layout(
            title='Wind Direction Overlay',
            geo=dict(
                showland=True,
                showcountries=True,
                showocean=True,
                countrywidth=0.5,
                landcolor='rgb(243, 243, 243)',
                oceancolor='rgb(204, 229, 255)',
                projection_scale=1
            )
        )
        return fig
