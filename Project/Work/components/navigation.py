"""Sidebar navigation component for the SLM Training Platform UI."""

import streamlit as st


def render_navigation():
    """Render the sidebar navigation."""
    st.sidebar.title("SLM Training Platform")
    st.sidebar.markdown("---")
    
    # Navigation items
    nav_items = [
        ("Home", "home"),
        ("Datasets", "datasets"),
        ("Models", "models"),
        ("Experiments", "experiments"),
        ("Evaluations", "evaluations"),
        ("Train Model", "train_model")
    ]
    
    # Initialize session state for current page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    # Render navigation buttons
    for label, page_key in nav_items:
        if st.sidebar.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
    
    st.sidebar.markdown("---")
    
    # Display current page indicator
    current_label = next((label for label, key in nav_items if key == st.session_state.current_page), "Home")
    st.sidebar.caption(f"Current: {current_label}")


def get_current_page() -> str:
    """Get the current page from session state."""
    return st.session_state.get("current_page", "home")


def set_current_page(page: str):
    """Set the current page in session state."""
    st.session_state.current_page = page
