"""Models page for browsing available base models and trained models."""

import streamlit as st
import pandas as pd
from services import model_service
from services.api_client import APIError
from components import loading_spinner, error_message, empty_state
from utils.formatters import format_date, format_number


def render():
    """Render the Models page."""
    st.title("Models")
    st.markdown("Browse available base models and fine-tuned models.")
    
    # Filter
    filter_type = st.selectbox(
        "Filter by Type",
        ["All", "Base", "Fine-tuned"],
        key="model_filter"
    )
    
    try:
        with loading_spinner.render_loading_container("Loading models..."):
            if filter_type == "All":
                models = model_service.get_models()
            elif filter_type == "Base":
                models = model_service.get_models(model_type="base")
            else:  # Fine-tuned
                models = model_service.get_models(model_type="fine_tuned")
    except APIError as e:
        error_message.render_api_error(e, show_retry=True, retry_callback=render)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    if not models:
        empty_state.render_empty_state(
            "No models available.",
            icon="🤖"
        )
        return
    
    # Models table
    st.subheader(f"Models ({len(models)} total)")
    
    # Prepare table data
    table_data = []
    for model in models:
        model_type = model.get("model_type", "N/A")
        if model_type == "fine_tuned":
            model_type_display = "Fine-tuned"
        else:
            model_type_display = "Base"
        
        table_data.append({
            "Name": model.get("name", "N/A"),
            "Type": model_type_display,
            "Version": model.get("version", "N/A"),
            "Architecture": model.get("architecture", "N/A"),
            "Parameters": format_number(model.get("parameters_count")),
            "Created": format_date(model.get("created_at")),
            "ID": model.get("id", "N/A")
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
    
    # Model detail drawer
    st.markdown("---")
    st.subheader("Model Details")
    
    if selected_indices and "selection" in selected_indices and selected_indices["selection"]["rows"]:
        selected_idx = selected_indices["selection"]["rows"][0]
        selected_model = models[selected_idx]
        
        # Fetch full model details
        model_id = selected_model.get("id")
        if model_id:
            try:
                with loading_spinner.render_loading_container("Loading model details..."):
                    model_details = model_service.get_model(model_id)
                
                # Display details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {model_details.get('name', 'N/A')}")
                    st.markdown(f"**Type:** {model_details.get('model_type', 'N/A').title()}")
                    st.markdown(f"**Version:** {model_details.get('version', 'N/A')}")
                    st.markdown(f"**Architecture:** {model_details.get('architecture', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Parameters:** {format_number(model_details.get('parameters_count'))}")
                    st.markdown(f"**Created:** {format_date(model_details.get('created_at'))}")
                    if model_details.get('is_latest_version'):
                        st.markdown("**Latest Version:** ✅ Yes")
                    else:
                        st.markdown("**Latest Version:** ❌ No")
                
                # Description
                if model_details.get("description"):
                    st.markdown("---")
                    st.markdown("**Description:**")
                    st.markdown(model_details.get("description"))
                
                # Metadata
                if model_details.get("metadata"):
                    st.markdown("---")
                    st.markdown("**Metadata:**")
                    st.json(model_details.get("metadata"))
                
                # Linked evaluations
                if model_details.get("linked_evaluations"):
                    st.markdown("---")
                    st.markdown("**Linked Evaluations:**")
                    evaluations = model_details.get("linked_evaluations", [])
                    if isinstance(evaluations, list):
                        for eval_id in evaluations:
                            st.markdown(f"- {eval_id}")
                    else:
                        st.json(evaluations)
                
            except APIError as e:
                error_message.render_api_error(e)
            except Exception as e:
                error_message.render_error_message(e)
    else:
        st.info("👆 Select a model from the table above to view details.")
