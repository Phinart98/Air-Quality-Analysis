import streamlit as st

def main():
    st.set_page_config(
        page_title="Air Quality Analysis Dashboard",
        page_icon="🌍",
        layout="wide"
    )
    
    from dashboard import create_dashboard
    create_dashboard()

if __name__ == "__main__":
    main()
