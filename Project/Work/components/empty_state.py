"""Empty state component for displaying when no data is available."""

import streamlit as st


def render_empty_state(
    message: str,
    action_label: str = None,
    action_callback=None,
    icon: str = "📭"
):
    """
    Render an empty state message with optional action button.
    
    Args:
        message: Message to display
        action_label: Label for action button (optional)
        action_callback: Callback function for action button (optional)
        icon: Icon to display (optional)
    """
    st.markdown("---")
    st.markdown(f"### {icon}")
    st.markdown(f"**{message}**")
    
    if action_label and action_callback:
        st.markdown("---")
        if st.button(action_label, use_container_width=True):
            action_callback()
