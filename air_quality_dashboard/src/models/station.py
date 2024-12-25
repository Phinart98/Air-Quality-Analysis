import streamlit as st

def render_sidebar():
    st.sidebar.title("Air Quality Analysis")
    
    analysis_view = st.sidebar.selectbox(
        "Select View",
        ["Station Density", "Station Locations", "Time Series"]
    )
    
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        ['US', 'GB', 'TR', 'TH', 'PH', 'IN'],
        default=['US', 'GB', 'TR', 'TH', 'PH', 'IN']
    )
    
    return analysis_view
