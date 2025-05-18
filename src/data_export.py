import streamlit as st
import pandas as pd
import json
import base64
import io
from datetime import datetime

def get_csv_download_link(df, filename="data.csv", button_text="Download CSV"):
    """
    Generate a download link for a DataFrame as CSV.
    
    Args:
        df (pandas.DataFrame): The DataFrame to export
        filename (str): The name of the file to download
        button_text (str): Text to display on the download button
        
    Returns:
        None: Displays a download button directly
    """
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{button_text}</a>'
    return st.markdown(href, unsafe_allow_html=True)

def get_excel_download_link(df, filename="data.xlsx", button_text="Download Excel"):
    """
    Generate a download link for a DataFrame as Excel.
    
    Args:
        df (pandas.DataFrame): The DataFrame to export
        filename (str): The name of the file to download
        button_text (str): Text to display on the download button
        
    Returns:
        None: Displays a download button directly
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Data', index=True)
    
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{button_text}</a>'
    return st.markdown(href, unsafe_allow_html=True)

def get_json_download_link(df, filename="data.json", button_text="Download JSON"):
    """
    Generate a download link for a DataFrame as JSON.
    
    Args:
        df (pandas.DataFrame): The DataFrame to export
        filename (str): The name of the file to download
        button_text (str): Text to display on the download button
        
    Returns:
        None: Displays a download button directly
    """
    json_str = df.to_json(orient='records', date_format='iso')
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">{button_text}</a>'
    return st.markdown(href, unsafe_allow_html=True)

def add_export_section(df, section_name="data"):
    """
    Add export functionality to a section of the dashboard.
    
    Args:
        df (pandas.DataFrame): The DataFrame to export
        section_name (str): Name of the section (used for filenames)
        
    Returns:
        None: Displays export options directly
    """
    if df is None or df.empty:
        st.warning("No data available to export.")
        return
    
    st.subheader("Export Data")
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"air_quality_{section_name}_{timestamp}"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        get_csv_download_link(df, filename=f"{filename_base}.csv", button_text="📄 Download CSV")
    
    with col2:
        get_excel_download_link(df, filename=f"{filename_base}.xlsx", button_text="📊 Download Excel")
    
    with col3:
        get_json_download_link(df, filename=f"{filename_base}.json", button_text="🔄 Download JSON")
    
    # Preview of data
    with st.expander("Preview Data"):
        st.dataframe(df.head(10))
        st.info(f"Showing 10 of {len(df)} rows. Download the full dataset using the buttons above.")

def export_map_as_html(m, filename="map.html"):
    """
    Provide a download link for a Folium map as HTML.
    
    Args:
        m (folium.Map): The Folium map to export
        filename (str): The name of the file to download
        
    Returns:
        None: Displays a download button directly
    """
    html_string = m._repr_html_()
    b64 = base64.b64encode(html_string.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}">🗺️ Download Interactive Map</a>'
    return st.markdown(href, unsafe_allow_html=True)
