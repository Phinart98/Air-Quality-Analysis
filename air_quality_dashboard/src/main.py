import streamlit as st
from utils.data_processor import DataProcessor
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from analytics.statistical_analysis import StatisticalAnalyzer
from analytics.trend_detection import TrendDetector
from analytics.forecasting import TimeSeriesForecaster
from visualization.heatmap import PollutionHeatmap

def main():
    st.set_page_config(
        page_title="Air Quality Analysis",
        page_icon="🌍",
        layout="wide"
    )
    
    if 'data_processor' not in st.session_state:
        data_processor = DataProcessor()
        data_processor.load_data()
        st.session_state.data_processor = data_processor
        
        # Initialize analytics components
        st.session_state.statistical_analyzer = StatisticalAnalyzer(data_processor.stations_data)
        st.session_state.trend_detector = TrendDetector()
        st.session_state.forecaster = TimeSeriesForecaster()
        st.session_state.heatmap = PollutionHeatmap(data_processor.stations_data)
    
    st.session_state.view_settings = render_sidebar()
    render_dashboard()

if __name__ == "__main__":
    main()
