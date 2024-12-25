import folium
from folium import plugins

def style_function(feature):
    return {
        'fillColor': 'transparent',
        'color': 'black',
        'weight': 1
    }

def create_station_map(stations_data, countries_data):
    m = folium.Map(
        location=[stations_data.geometry.y.mean(), stations_data.geometry.x.mean()],
        zoom_start=4,
        tiles='CartoDB positron'
    )
    
    folium.GeoJson(
        countries_data,
        style_function=style_function
    ).add_to(m)
    
    marker_cluster = plugins.MarkerCluster().add_to(m)
    
    for idx, row in stations_data.iterrows():
        folium.Marker(
            [row.geometry.y, row.geometry.x],
            popup=f"Station ID: {row['id']}<br>Country: {row['country_id']}<br>PM10: {row['pm10']}"
        ).add_to(marker_cluster)
    
    return m
