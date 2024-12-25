import streamlit as st
from visualization.maps import create_station_map
from visualization.time_series import create_time_series_chart
from visualization.charts import create_density_chart
from visualization.correlation_matrix import CorrelationMatrix

def render_dashboard():
    view_settings = st.session_state.get('view_settings', {})
    analysis_type = view_settings.get('analysis_type', 'Station Density')
    
    if analysis_type == "Station Density":
        st.subheader("Station Density Analysis")
        if st.session_state.data_processor.density_results is not None:
            st.plotly_chart(create_density_chart(st.session_state.data_processor.density_results), use_container_width=True)
            
        st.subheader("Statistical Summary")
        if st.session_state.data_processor.stations_data is not None:
            valid_data = st.session_state.data_processor.stations_data[
                st.session_state.data_processor.stations_data['pm10'].notna()
            ]
            if not valid_data.empty:
                stats = st.session_state.statistical_analyzer.compute_basic_stats('pm10')
                for key, value in stats.items():
                    st.metric(label=key.capitalize(), value=f"{value:.2f}")
    
    elif analysis_type == "Station Locations":
        st.subheader("Station Locations")
        
        @st.cache_data
        def get_map():
            return create_station_map(
                st.session_state.data_processor.stations_data,
                st.session_state.data_processor.countries_data
            )
            
        @st.cache_data
        def get_heatmap():
            return st.session_state.heatmap.create_heatmap()
        
        tab1, tab2 = st.tabs(["Map View", "Heat Map"])
        with tab1:
            st.components.v1.html(get_map()._repr_html_(), height=600)
        with tab2:
            st.components.v1.html(get_heatmap()._repr_html_(), height=600)
    
    elif analysis_type == "Time Series":
        st.subheader("Time Series Analysis")
        
        @st.cache_data
        def get_stations():
            return st.session_state.data_processor.stations_data['id'].unique().tolist()
        
        selected_station = st.selectbox("Select Station", get_stations())
        if selected_station:
            with st.spinner('Loading time series data...'):
                time_data = st.session_state.data_processor.get_time_series_data(selected_station)
                if time_data is not None and not time_data.empty:
                    st.plotly_chart(create_time_series_chart(time_data), use_container_width=True)
                else:
                    st.error("No data available for this station")
    
    elif analysis_type == "Analytics":
        st.subheader("Analytics")
        
        @st.cache_data
        def get_correlation_matrix():
            corr_matrix = CorrelationMatrix(st.session_state.data_processor.stations_data)
            return corr_matrix.create_correlation_matrix()
            
        st.pyplot(get_correlation_matrix())
