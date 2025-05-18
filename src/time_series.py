import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from datetime import datetime, timedelta
import math
import random

def fetch_historical_data(station_id, pollutant, days=30):
    """
    Fetch historical pollutant data for a specific station.
    
    Args:
        station_id (str): The ID of the monitoring station
        pollutant (str): The pollutant code (pm10, pm25, etc.)
        days (int): Number of days of historical data to fetch
        
    Returns:
        pandas.DataFrame: Time series data with datetime index and pollutant values
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Format dates for API
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    # Try the main API endpoint first
    base_url = "https://api.energyandcleanair.org/measurements"  # Removed /v1/
    params = {
        "station_id": station_id,
        "pollutant": pollutant,
        "start_date": start_str,
        "end_date": end_str,
        "format": "json",  # Added format parameter
        "limit": 1000
    }
    
    try:
        st.info(f"Fetching data from {base_url} with parameters: {params}")
        response = requests.get(base_url, params=params, timeout=15)
        
        # Debug information
        st.info(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            # Try alternative endpoint format
            alt_base_url = f"https://api.energyandcleanair.org/stations/{station_id}/measurements"
            alt_params = {
                "pollutant": pollutant,
                "start_date": start_str,
                "end_date": end_str,
                "format": "json",
                "limit": 1000
            }
            
            st.info(f"Trying alternative endpoint: {alt_base_url}")
            response = requests.get(alt_base_url, params=alt_params, timeout=15)
            st.info(f"Alternative response status code: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame
        if "results" in data and len(data["results"]) > 0:
            df = pd.DataFrame(data["results"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index("datetime")
            return df
        elif isinstance(data, list) and len(data) > 0:
            # Handle case where API returns a list directly
            df = pd.DataFrame(data)
            if "date" in df.columns:
                df["datetime"] = pd.to_datetime(df["date"])
            elif "timestamp" in df.columns:
                df["datetime"] = pd.to_datetime(df["timestamp"])
            else:
                st.warning("Could not find date column in response")
                return pd.DataFrame()
                
            df = df.set_index("datetime")
            return df
        else:
            st.warning(f"API returned empty or unexpected data structure: {data}")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        
        # For development/testing: create mock data
        st.info("Generating mock data for demonstration purposes")
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        mock_values = [10 + 5 * math.sin(i/24 * math.pi) + random.uniform(-2, 2) for i in range(len(dates))]
        
        mock_df = pd.DataFrame({
            'datetime': dates,
            'value': mock_values,
            'pollutant': pollutant,
            'station_name': f"Station {station_id}"
        })
        mock_df = mock_df.set_index('datetime')
        return mock_df


def plot_time_series(df, pollutant_info):
    """
    Create a time series plot for pollutant data.
    
    Args:
        df (pandas.DataFrame): DataFrame with datetime index and pollutant values
        pollutant_info (dict): Dictionary with pollutant metadata
        
    Returns:
        plotly.graph_objects.Figure: Interactive time series plot
    """
    if df.empty:
        st.warning("No historical data available for the selected station and pollutant.")
        return None
    
    pollutant = df["pollutant"].iloc[0]
    station_name = df["station_name"].iloc[0] if "station_name" in df.columns else "Unknown Station"
    
    # Get pollutant info
    p_name = pollutant_info.get(pollutant, {}).get("name", pollutant.upper())
    p_unit = pollutant_info.get(pollutant, {}).get("unit", "")
    p_color = pollutant_info.get(pollutant, {}).get("color", "blue")
    
    # Create plot
    fig = px.line(
        df, 
        y="value",
        title=f"{p_name} Levels at {station_name}",
        labels={"value": f"Concentration ({p_unit})", "datetime": "Date"},
        color_discrete_sequence=[p_color]
    )
    
    # Add rolling average
    df_rolling = df.copy()
    df_rolling["24h_avg"] = df["value"].rolling(window=24).mean()
    
    fig.add_scatter(
        x=df_rolling.index, 
        y=df_rolling["24h_avg"],
        mode="lines",
        name="24-hour Moving Average",
        line=dict(width=2, dash="dash")
    )
    
    return fig

def add_time_series_section(stations_gdf, pollutant_info):
    """
    Add time series analysis section to the dashboard.
    
    Args:
        stations_gdf (geopandas.GeoDataFrame): GeoDataFrame with station data
        pollutant_info (dict): Dictionary with pollutant metadata
    """
    st.header("📈 Time Series Analysis")
    
    # Station selection
    station_options = []
    for _, row in stations_gdf.iterrows():
        if row["name"] and row["id"]:
            station_options.append({
                "id": row["id"],
                "name": f"{row['name']} ({row['city_name'] if row['city_name'] else 'Unknown City'}, {row['country_id']})"
            })
    
    if not station_options:
        st.warning("No stations available for time series analysis.")
        return
    
    selected_station = st.selectbox(
        "Select a monitoring station:",
        options=station_options,
        format_func=lambda x: x["name"]
    )
    
    # Pollutant selection
    station_row = stations_gdf[stations_gdf["id"] == selected_station["id"]].iloc[0]
    available_pollutants = station_row["pollutants"] if isinstance(station_row["pollutants"], list) else []
    
    if not available_pollutants:
        st.warning("No pollutant data available for the selected station.")
        return
    
    selected_pollutant = st.selectbox(
        "Select pollutant to analyze:",
        options=[p for p in available_pollutants if p in pollutant_info],
        format_func=lambda p: pollutant_info[p]["name"]
    )
    
    # Time range selection
    time_range = st.slider(
        "Select time range (days):",
        min_value=7,
        max_value=90,
        value=30,
        step=1
    )
    
    # Fetch and display data
    with st.spinner("Fetching historical data..."):
        df = fetch_historical_data(
            selected_station["id"],
            selected_pollutant,
            days=time_range
        )
    
    if not df.empty:
        fig = plot_time_series(df, pollutant_info)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Basic statistics
            st.subheader("Statistical Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Average", 
                    f"{df['value'].mean():.2f} {pollutant_info[selected_pollutant]['unit']}"
                )
            
            with col2:
                st.metric(
                    "Maximum", 
                    f"{df['value'].max():.2f} {pollutant_info[selected_pollutant]['unit']}"
                )
                
            with col3:
                st.metric(
                    "Minimum", 
                    f"{df['value'].min():.2f} {pollutant_info[selected_pollutant]['unit']}"
                )
    else:
        st.warning("No data available for the selected parameters.")
