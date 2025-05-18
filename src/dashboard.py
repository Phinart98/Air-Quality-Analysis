import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static
import plotly.express as px
import pandas as pd
import geopandas as gpd
import requests
from datetime import datetime, timedelta
from time_series import add_time_series_section

def get_pollutant_info():
    return {
        "pm10": {"name": "Particulate Matter (PM10)", "unit": "μg/m³", "color": "red", 
                 "description": "Inhalable particles with diameters of 10 micrometers and smaller"},
        "pm25": {"name": "Fine Particulate Matter (PM2.5)", "unit": "μg/m³", "color": "purple",
                 "description": "Fine inhalable particles with diameters of 2.5 micrometers and smaller"},
        "no2": {"name": "Nitrogen Dioxide (NO₂)", "unit": "ppb", "color": "orange",
                "description": "Toxic gas from vehicle exhaust and power plants"},
        "so2": {"name": "Sulfur Dioxide (SO₂)", "unit": "ppb", "color": "blue",
                "description": "Toxic gas from fossil fuel combustion and industrial processes"},
        "o3": {"name": "Ozone (O₃)", "unit": "ppb", "color": "green",
               "description": "Ground-level ozone created by chemical reactions between oxides of nitrogen and VOCs"},
        "co": {"name": "Carbon Monoxide (CO)", "unit": "ppm", "color": "brown",
               "description": "Toxic gas from vehicle exhaust and incomplete combustion"}
    }

def get_regions():
    return {
        "Asia": ["IN", "PH", "TH", "MY", "ID", "JP", "KR", "CN", "VN", "LK"],
        "Europe": ["GB", "FR", "DE", "IT", "ES", "TR", "PL", "NL", "BE", "SE"],
        "North America": ["US", "CA", "MX"],
        "South America": ["BR", "AR", "CL", "CO", "PE"],
        "Africa": ["ZA", "NG", "EG", "KE", "MA"],
        "Oceania": ["AU", "NZ", "FJ"]
    }

def get_country_codes():
    return {
        "US": "United States", "GB": "United Kingdom", "TR": "Turkey",
        "PH": "Philippines", "IN": "India", "TH": "Thailand",
        "MY": "Malaysia", "ID": "Indonesia", "JP": "Japan",
        "KR": "South Korea", "CN": "China", "FR": "France",
        "DE": "Germany", "IT": "Italy", "ES": "Spain"
    }

def fetch_station_data(countries=None):
    base_url = "https://api.energyandcleanair.org/stations"
    params = {"format": "geojson"}
    if countries:
        params["country"] = ",".join(countries)
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out. The server might be experiencing high load.")
        return {"type": "FeatureCollection", "features": []}
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}")
        return {"type": "FeatureCollection", "features": []}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {"type": "FeatureCollection", "features": []}
    except ValueError:
        st.error("Invalid response format. Could not parse JSON.")
        return {"type": "FeatureCollection", "features": []}


@st.cache_data(ttl=3600)
def load_data(selected_countries):
    stations_data = fetch_station_data(selected_countries)
    stations_gdf = gpd.GeoDataFrame.from_features(stations_data['features'])
    return stations_gdf

def create_dashboard():
    st.title("🌍 Air Quality Monitoring Network Analysis")
    
    # Sidebar configuration
    st.sidebar.header("Analysis Filters")
    
    # Region and country selection
    regions = get_regions()
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=list(regions.keys()),
        default=["Asia"]
    )
    
    available_countries = []
    for region in selected_regions:
        available_countries.extend(regions[region])
    
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=sorted(available_countries),
        default=available_countries[:5]
    )
    
    # Pollutant selection
    pollutant_info = get_pollutant_info()
    selected_pollutants = st.sidebar.multiselect(
        "Select Pollutants",
        options=list(pollutant_info.keys()),
        default=["pm10", "pm25"],
        format_func=lambda x: pollutant_info[x]["name"]
    )
    
    # Load data
    with st.spinner("Loading monitoring station data..."):
        stations_gdf = load_data(selected_countries)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Network Overview",
        "Station Distribution",
        "Pollutant Analysis",
        "Time Series Analysis"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Monitoring Stations", len(stations_gdf))
        with col2:
            coverage = len(stations_gdf[
                stations_gdf['pollutants'].apply(
                    lambda x: any(p in x for p in selected_pollutants) if isinstance(x, list) else False
                )
            ])
            st.metric(f"Stations Measuring Selected Pollutants", coverage)
        
        st.subheader("Monitoring Station Network")
        
        # Create map
        m = folium.Map(location=[20, 0], zoom_start=2)
        marker_cluster = plugins.MarkerCluster()
        
        # Add stations to map
        for _, row in stations_gdf.iterrows():
            pollutants = row['pollutants'] if isinstance(row['pollutants'], list) else []
            if any(p in pollutants for p in selected_pollutants):
                color = next((pollutant_info[p]["color"] for p in selected_pollutants if p in pollutants), "gray")
                
                popup_content = f"""
                <div style='min-width: 200px'>
                    <h4>{row['name']}</h4>
                    <b>Location:</b> {row['city_name']}, {get_country_codes().get(row['country_id'], row['country_id'])}<br>
                    <b>Pollutants Measured:</b><br>
                """
                for p in pollutants:
                    if p in pollutant_info:
                        popup_content += f"• {pollutant_info[p]['name']} ({pollutant_info[p]['unit']})<br>"
                popup_content += "</div>"
                
                folium.CircleMarker(
                    location=[row.geometry.y, row.geometry.x],
                    radius=8,
                    color=color,
                    fill=True,
                    popup=folium.Popup(popup_content, max_width=300)
                ).add_to(marker_cluster)
        
        marker_cluster.add_to(m)
        
        # Display full-width map
        st.components.v1.html(m._repr_html_(), height=600)
        
        # Pollutant legend
        st.markdown("### Monitored Pollutants Information")
        cols = st.columns(2)
        for idx, (code, info) in enumerate(pollutant_info.items()):
            col = cols[idx % 2]
            with col:
                st.markdown(
                    f"<div style='color:{info['color']};'>"
                    f"<h4>●  {info['name']}</h4>"
                    f"<p>Unit: {info['unit']}<br>"
                    f"{info['description']}</p></div>",
                    unsafe_allow_html=True
                )
    
    with tab2:
        st.subheader("Geographic Distribution Analysis")
        
        # Country-level analysis
        country_data = stations_gdf['country_id'].value_counts().reset_index()
        country_data.columns = ['Country', 'Station Count']
        country_data['Country'] = country_data['Country'].map(get_country_codes())
        country_data = country_data.dropna(subset=['Country'])
        
        fig = px.bar(
            country_data,
            x='Country',
            y='Station Count',
            title='Monitoring Stations by Country',
            color='Station Count',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # City-level analysis
        st.subheader("City-level Distribution")
        selected_country = st.selectbox(
            "Select Country for Detailed Analysis",
            options=[c for c in country_data['Country'].tolist() if pd.notna(c)]
        )
        
        if selected_country and selected_country in {v: k for k, v in get_country_codes().items()}:
            country_code = {v: k for k, v in get_country_codes().items()}[selected_country]
            city_data = stations_gdf[stations_gdf['country_id'] == country_code]
            city_data = city_data[city_data['city_name'].notna()]
            city_counts = city_data.groupby('city_name').size().reset_index()
            city_counts.columns = ['City', 'Station Count']
            
            fig = px.treemap(
                city_counts,
                path=['City'],
                values='Station Count',
                title=f'Monitoring Station Distribution in {selected_country}'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Pollutant Coverage Analysis")
        
        pollutant_data = []
        for _, row in stations_gdf.iterrows():
            station_pollutants = row['pollutants'] if isinstance(row['pollutants'], list) else []
            for pollutant in station_pollutants:
                if pollutant in pollutant_info:
                    pollutant_data.append({
                        'Country': get_country_codes().get(row['country_id'], row['country_id']),
                        'Pollutant': pollutant_info[pollutant]['name']
                    })
        
        pollutant_df = pd.DataFrame(pollutant_data)
        
        fig = px.histogram(
            pollutant_df,
            x='Country',
            color='Pollutant',
            barmode='group',
            title='Pollutant Measurement Capabilities by Country',
            labels={'count': 'Number of Stations'}
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab4:
        add_time_series_section(stations_gdf, pollutant_info)

if __name__ == "__main__":
    create_dashboard()
