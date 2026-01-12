"""Home/Dashboard page for the SLM Training Platform UI."""

import streamlit as st
import pandas as pd
from services import dataset_service, model_service, experiment_service
from services.api_client import APIError
from components import loading_spinner, error_message, empty_state
from utils.formatters import format_date


def render():
    """Render the Home/Dashboard page."""
    st.title("Dashboard")
    st.markdown("Welcome to the SLM Training Platform. Here's an overview of your system.")
    
    # Load data
    try:
        with loading_spinner.render_loading_container("Loading dashboard data..."):
            datasets = dataset_service.get_datasets()
            models = model_service.get_models()
            experiments = experiment_service.get_experiments()
    except APIError as e:
        error_message.render_api_error(e, show_retry=True, retry_callback=render)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    # Summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Datasets", len(datasets))
    
    with col2:
        st.metric("Total Models", len(models))
    
    with col3:
        st.metric("Total Experiments", len(experiments))
    
    st.markdown("---")
    
    # Recent experiments table
    st.subheader("Recent Experiments")
    
    if not experiments:
        empty_state.render_empty_state(
            "No experiments yet.",
            action_label="Create New Experiment",
            action_callback=lambda: st.session_state.update({"current_page": "train_model"})
        )
    else:
        # Sort by created_at descending and take last 5
        sorted_experiments = sorted(
            experiments,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:5]
        
        # Prepare data for table
        table_data = []
        for exp in sorted_experiments:
            table_data.append({
                "Name": exp.get("name", "N/A"),
                "Status": exp.get("status", "N/A"),
                "Created": format_date(exp.get("created_at"))
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Link to experiments page
        if st.button("View All Experiments", use_container_width=True):
            st.session_state.current_page = "experiments"
            st.rerun()
