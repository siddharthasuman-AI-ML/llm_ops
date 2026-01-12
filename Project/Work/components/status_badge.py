"""Status badge component for displaying experiment status."""

import streamlit as st


STATUS_COLORS = {
    "created": "⚪",
    "running": "🟡",
    "completed": "🟢",
    "failed": "🔴",
    "cancelled": "⚫"
}

STATUS_LABELS = {
    "created": "Created",
    "running": "Running",
    "completed": "Completed",
    "failed": "Failed",
    "cancelled": "Cancelled"
}


def render_status_badge(status: str):
    """
    Render a status badge with color coding.
    
    Args:
        status: Status string (created, running, completed, failed, cancelled)
    """
    status_lower = status.lower() if status else "unknown"
    
    emoji = STATUS_COLORS.get(status_lower, "⚪")
    label = STATUS_LABELS.get(status_lower, status_lower.title())
    
    st.markdown(f"{emoji} **{label}**")
