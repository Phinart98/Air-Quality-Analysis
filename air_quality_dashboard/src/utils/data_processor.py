import requests
import geopandas as gpd
import pandas as pd
import streamlit as st

class DataProcessor:
    def __init__(self):
        self.stations_data = None
        self.countries_data = None
        self.density_results = None
        self.time_series_data = None

    @st.cache_data(ttl=3600)
    def load_data(self, selected_countries=None):
        if not selected_countries:
            selected_countries = ['US', 'GB', 'TR', 'PH', 'IN', 'TH']
            
        countries_str = ','.join(selected_countries)
        stations_url = f"https://api.energyandcleanair.org/stations?country={countries_str}&format=geojson"
        countries_url = "https://r2.datahub.io/clvyjaryy0000la0cxieg4o8o/main/raw/data/countries.geojson"
        
        stations = requests.get(stations_url).json()
        countries = requests.get(countries_url).json()
        
        self.stations_data = self.process_station_data(stations)
        self.countries_data = gpd.GeoDataFrame.from_features(countries['features'])
        
        self.stations_data.set_crs(epsg=4326, inplace=True)
        self.countries_data.set_crs(epsg=4326, inplace=True)
        
        self.calculate_densities(selected_countries)

    def process_station_data(self, stations_json):
        stations_gdf = gpd.GeoDataFrame.from_features(stations_json['features'])
        
        def get_pollutant_value(pollutants, parameter):
            if isinstance(pollutants, list):
                for p in pollutants:
                    if isinstance(p, dict) and p.get('parameter') == parameter:
                        return float(p.get('value', 0))
            return 0.0
        
        stations_gdf['pm10'] = stations_gdf['pollutants'].apply(
            lambda x: get_pollutant_value(x, 'pm10')
        )
        stations_gdf['pm25'] = stations_gdf['pollutants'].apply(
            lambda x: get_pollutant_value(x, 'pm25')
        )
        
        stations_gdf['timestamp'] = pd.to_datetime(stations_gdf['last_update'])
        return stations_gdf

    def calculate_densities(self, selected_countries):
        country_codes = {
            'US': 'USA',
            'GB': 'GBR',
            'TR': 'TUR',
            'TH': 'THA',
            'PH': 'PHL',
            'IN': 'IND'
        }
        
        countries_proj = self.countries_data.to_crs('ESRI:54009')
        countries_proj['area_sqkm'] = countries_proj.geometry.area / 10**6
        
        station_counts = self.stations_data.groupby('country_id').size()
        
        results = []
        for country_code_2 in selected_countries:
            country_code_3 = country_codes[country_code_2]
            country_area = countries_proj[countries_proj['ISO_A3'] == country_code_3]['area_sqkm'].iloc[0]
            station_count = station_counts.get(country_code_2, 0)
            density = (station_count / country_area) * 1000
            
            results.append({
                'Country': country_code_2,
                'PM10_Stations': station_count,
                'Area_sqkm': round(country_area, 2),
                'Density_per_1000sqkm': round(density, 4)
            })
        
        self.density_results = pd.DataFrame(results)

    @st.cache_data(ttl=3600)
    def get_time_series_data(self, station_id):
        url = f"https://api.energyandcleanair.org/measurements?station_id={station_id}&parameter=pm10&limit=1000"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return None
