"""Main Streamlit application entry point for SLM Training Platform UI."""

import streamlit as st
import sys
import os

# Add the work directory to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components import navigation
from pages import home, datasets, models, experiments, evaluations, train_model
from utils.config import validate_config
from services.api_client import APIError


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="SLM Training Platform",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Validate configuration
    config_valid, config_error = validate_config()
    if not config_valid:
        st.error(f"⚠️ Configuration Error: {config_error}")
        st.info("Please create a `.env` file in the project root with `API_BASE_URL=http://localhost:8000`")
        st.stop()
    
    # Render navigation
    navigation.render_navigation()
    
    # Get current page
    current_page = navigation.get_current_page()
    
    # Route to appropriate page
    try:
        if current_page == "home":
            home.render()
        elif current_page == "datasets":
            datasets.render()
        elif current_page == "models":
            models.render()
        elif current_page == "experiments":
            experiments.render()
        elif current_page == "evaluations":
            evaluations.render()
        elif current_page == "train_model":
            train_model.render()
        else:
            # Default to home
            navigation.set_current_page("home")
            home.render()
    except APIError as e:
        # Global API error handling
        st.error(f"API Error: {e.message}")
        if e.status_code:
            st.caption(f"Status Code: {e.status_code}")
    except Exception as e:
        # Global error handling
        st.error(f"An unexpected error occurred: {str(e)}")
        st.caption("Please check the console for more details.")


if __name__ == "__main__":
    main()
