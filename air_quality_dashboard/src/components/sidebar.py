import streamlit as st

def render_sidebar():
    st.sidebar.title("Analysis Settings")
    
    country_codes = {
        'US': 'United States',
        'GB': 'United Kingdom',
        'TR': 'Turkey',
        'TH': 'Thailand',
        'PH': 'Philippines',
        'IN': 'India'
    }
    
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=list(country_codes.keys()),
        default=list(country_codes.keys()),
        format_func=lambda x: country_codes[x]
    )
    
    analysis_type = st.sidebar.selectbox(
        "Analysis Type",
        ["Station Density", "Station Locations", "Time Series", "Analytics"]
    )
    
    return {
        'selected_countries': selected_countries,
        'analysis_type': analysis_type
    }
