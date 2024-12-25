import plotly.express as px

def create_time_series_chart(data):
    fig = px.line(
        data,
        x='timestamp',
        y='value',
        title='Air Quality Time Series'
    )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Pollutant Value",
        showlegend=True
    )
    
    return fig
