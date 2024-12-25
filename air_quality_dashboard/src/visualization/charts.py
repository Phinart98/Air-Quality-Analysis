import plotly.express as px

def create_density_chart(density_df):
    fig = px.bar(
        data_frame=density_df,
        x='Country',
        y='Density_per_1000sqkm',
        title='PM10 Monitoring Station Density by Country',
        labels={
            'Density_per_1000sqkm': 'Stations per 1,000 km²',
            'Country': ''
        }
    )
    
    fig.update_layout(
        height=500,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig

def create_time_series_chart(time_data):
    fig = px.line(
        data_frame=time_data,
        x='timestamp',
        y='value',
        title='PM10 Levels Over Time',
        labels={'value': 'PM10 (µg/m³)', 'timestamp': 'Date'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_title='Date',
        yaxis_title='PM10 (µg/m³)'
    )
    
    return fig
