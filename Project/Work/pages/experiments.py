"""Experiments page for tracking training runs and their status."""

import streamlit as st
import pandas as pd
import time
from services import experiment_service
from services.api_client import APIError
from components import loading_spinner, error_message, empty_state, status_badge
from utils.formatters import format_date


def render():
    """Render the Experiments page."""
    st.title("Experiments")
    st.markdown("Track your training runs and monitor their status.")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (every 5 seconds)", value=False, key="auto_refresh")
    
    # Load experiments
    try:
        with loading_spinner.render_loading_container("Loading experiments..."):
            experiments = experiment_service.get_experiments()
    except APIError as e:
        error_message.render_api_error(e, show_retry=True, retry_callback=render)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    if not experiments:
        empty_state.render_empty_state(
            "No experiments yet.",
            action_label="Create New Experiment",
            action_callback=lambda: st.session_state.update({"current_page": "train_model"})
        )
        return
    
    # Auto-refresh logic
    if auto_refresh:
        # Check if we need to refresh
        if "last_refresh" not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        current_time = time.time()
        if current_time - st.session_state.last_refresh >= 5:
            st.session_state.last_refresh = current_time
            st.rerun()
        
        # Show refresh indicator
        st.caption(f"⏱️ Last refreshed: {time.strftime('%H:%M:%S')}")
    
    # Experiments table
    st.subheader(f"All Experiments ({len(experiments)} total)")
    
    # Prepare table data
    table_data = []
    for exp in experiments:
        table_data.append({
            "Name": exp.get("name", "N/A"),
            "Status": exp.get("status", "N/A"),
            "Base Model": exp.get("base_model_id", "N/A")[:8] + "..." if exp.get("base_model_id") else "N/A",
            "Dataset": exp.get("training_dataset_id", "N/A")[:8] + "..." if exp.get("training_dataset_id") else "N/A",
            "Created": format_date(exp.get("created_at")),
            "ID": exp.get("id", "N/A")
        })
    
    df = pd.DataFrame(table_data)
    
    # Display table with clickable rows
    selected_indices = st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Experiment detail view
    st.markdown("---")
    st.subheader("Experiment Details")
    
    if selected_indices and "selection" in selected_indices and selected_indices["selection"]["rows"]:
        selected_idx = selected_indices["selection"]["rows"][0]
        selected_experiment = experiments[selected_idx]
        
        # Fetch full experiment details
        experiment_id = selected_experiment.get("id")
        if experiment_id:
            try:
                with loading_spinner.render_loading_container("Loading experiment details..."):
                    exp_details = experiment_service.get_experiment(experiment_id)
                
                # Basic info
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {exp_details.get('name', 'N/A')}")
                    st.markdown(f"**Status:**")
                    status_badge.render_status_badge(exp_details.get('status', 'N/A'))
                    st.markdown(f"**Created:** {format_date(exp_details.get('created_at'))}")
                
                with col2:
                    st.markdown(f"**Base Model ID:** {exp_details.get('base_model_id', 'N/A')}")
                    st.markdown(f"**Training Dataset ID:** {exp_details.get('training_dataset_id', 'N/A')}")
                    if exp_details.get('eval_dataset_id'):
                        st.markdown(f"**Eval Dataset ID:** {exp_details.get('eval_dataset_id')}")
                
                # Description and goal
                if exp_details.get("description"):
                    st.markdown("---")
                    st.markdown("**Description:**")
                    st.markdown(exp_details.get("description"))
                
                if exp_details.get("goal"):
                    st.markdown("---")
                    st.markdown("**Goal:**")
                    st.markdown(exp_details.get("goal"))
                
                # Training config
                if exp_details.get("training_config"):
                    st.markdown("---")
                    st.markdown("**Training Configuration:**")
                    training_config = exp_details.get("training_config")
                    if isinstance(training_config, dict):
                        st.json(training_config)
                    else:
                        st.markdown(str(training_config))
                
                # Status timeline (simplified)
                st.markdown("---")
                st.markdown("**Status Timeline:**")
                status = exp_details.get("status", "created")
                statuses = ["created", "running", "completed", "failed", "cancelled"]
                current_idx = statuses.index(status) if status in statuses else 0
                
                timeline = ""
                for i, s in enumerate(statuses):
                    if i <= current_idx:
                        timeline += f"✅ {s.title()}\n"
                    else:
                        timeline += f"⏳ {s.title()}\n"
                
                st.markdown(timeline)
                
                # Links
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if exp_details.get("resulting_model_id"):
                        st.markdown(f"**Resulting Model:** {exp_details.get('resulting_model_id')}")
                        if st.button("View Model", key="view_model_btn"):
                            st.session_state.current_page = "models"
                            st.session_state.selected_model_id = exp_details.get("resulting_model_id")
                            st.rerun()
                
                with col2:
                    if exp_details.get("id"):
                        st.markdown(f"**Evaluations:**")
                        if st.button("View Evaluations", key="view_evaluations_btn"):
                            st.session_state.current_page = "evaluations"
                            st.session_state.filter_experiment_id = exp_details.get("id")
                            st.rerun()
                
            except APIError as e:
                error_message.render_api_error(e)
            except Exception as e:
                error_message.render_error_message(e)
    else:
        st.info("👆 Select an experiment from the table above to view details.")
    
    # Manual refresh button
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.rerun()
