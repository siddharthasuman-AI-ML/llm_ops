"""Error message component for displaying user-friendly error messages."""

import streamlit as st
from services.api_client import APIError


def render_error_message(error: Exception, show_retry: bool = False, retry_callback=None):
    """
    Render a user-friendly error message.
    
    Args:
        error: Exception object
        show_retry: Whether to show a retry button
        retry_callback: Callback function for retry button
    """
    # Extract error message
    if isinstance(error, APIError):
        error_message = error.message
        if error.status_code:
            st.error(f"**Error {error.status_code}**: {error_message}")
        else:
            st.error(f"**Error**: {error_message}")
    else:
        # Generic error message - no stack traces
        error_message = str(error) if error else "An unexpected error occurred."
        st.error(f"**Error**: {error_message}")
    
    # Show retry button if requested
    if show_retry and retry_callback:
        if st.button("🔄 Retry", key="retry_button"):
            retry_callback()


def render_api_error(error: APIError, show_retry: bool = False, retry_callback=None):
    """
    Render an API error message specifically.
    
    Args:
        error: APIError object
        show_retry: Whether to show a retry button
        retry_callback: Callback function for retry button
    """
    if error.status_code == 404:
        st.warning("The requested resource was not found.")
    elif error.status_code == 400:
        st.error(f"**Invalid Request**: {error.message}")
    elif error.status_code == 500:
        st.error("**Server Error**: The server encountered an error. Please try again later.")
    elif error.status_code:
        st.error(f"**Error {error.status_code}**: {error.message}")
    else:
        st.error(f"**Error**: {error.message}")
    
    if show_retry and retry_callback:
        if st.button("🔄 Retry", key="retry_button"):
            retry_callback()
