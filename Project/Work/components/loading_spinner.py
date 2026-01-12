"""Loading spinner component for displaying loading states."""

import streamlit as st


def render_loading_spinner(message: str = "Loading..."):
    """
    Render a loading spinner with message.
    
    Args:
        message: Loading message to display
    """
    with st.spinner(message):
        st.empty()


def render_loading_container(message: str = "Loading..."):
    """
    Create a loading container context manager.
    
    Args:
        message: Loading message to display
        
    Returns:
        Context manager for loading state
    """
    return st.spinner(message)
