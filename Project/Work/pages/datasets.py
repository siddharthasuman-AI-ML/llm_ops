"""Datasets page for managing training and evaluation datasets."""

import streamlit as st
import pandas as pd
from services import dataset_service
from services.api_client import APIError
from components import loading_spinner, error_message, empty_state
from utils.validators import validate_required_field, validate_file_type, validate_dataset_type
from utils.formatters import format_date, format_number


def render():
    """Render the Datasets page."""
    st.title("Datasets")
    st.markdown("Manage your training and evaluation datasets.")
    
    # Upload form
    with st.expander("📤 Upload New Dataset", expanded=False):
        with st.form("upload_dataset_form"):
            dataset_name = st.text_input("Dataset Name *", placeholder="e.g., support_data_v1")
            description = st.text_area("Description", placeholder="Optional description of the dataset")
            dataset_type = st.selectbox("Dataset Type *", ["training", "evaluation"])
            uploaded_file = st.file_uploader(
                "Dataset File *",
                type=["csv", "json", "jsonl"],
                help="Upload CSV, JSON, or JSONL file"
            )
            
            submit_button = st.form_submit_button("Upload Dataset", use_container_width=True)
            
            if submit_button:
                # Validate form
                errors = []
                
                name_valid, name_error = validate_required_field(dataset_name, "Dataset name")
                if not name_valid:
                    errors.append(name_error)
                
                file_valid, file_error = validate_file_type(uploaded_file)
                if not file_valid:
                    errors.append(file_error)
                
                type_valid, type_error = validate_dataset_type(dataset_type)
                if not type_valid:
                    errors.append(type_error)
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Upload dataset
                    try:
                        with loading_spinner.render_loading_container("Uploading dataset..."):
                            result = dataset_service.upload_dataset(
                                file=uploaded_file,
                                name=dataset_name,
                                description=description or "",
                                dataset_type=dataset_type
                            )
                        
                        st.success(f"✅ Dataset '{result.get('name', dataset_name)}' uploaded successfully!")
                        st.balloons()
                        # Clear form by rerunning
                        st.rerun()
                    except APIError as e:
                        error_message.render_api_error(e)
                    except Exception as e:
                        error_message.render_error_message(e)
    
    st.markdown("---")
    
    # Datasets table
    st.subheader("All Datasets")
    
    try:
        with loading_spinner.render_loading_container("Loading datasets..."):
            datasets = dataset_service.get_datasets()
    except APIError as e:
        error_message.render_api_error(e, show_retry=True, retry_callback=render)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    if not datasets:
        empty_state.render_empty_state(
            "No datasets uploaded yet.",
            action_label="Upload Dataset",
            action_callback=lambda: st.session_state.update({"upload_expanded": True})
        )
        return
    
    # Pagination
    items_per_page = 10
    total_pages = (len(datasets) + items_per_page - 1) // items_per_page
    
    if "datasets_page" not in st.session_state:
        st.session_state.datasets_page = 1
    
    page = st.session_state.datasets_page
    
    # Page controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀ Previous", disabled=(page <= 1)):
            st.session_state.datasets_page = page - 1
            st.rerun()
    
    with col2:
        st.caption(f"Page {page} of {total_pages} ({len(datasets)} total datasets)")
    
    with col3:
        if st.button("Next ▶", disabled=(page >= total_pages)):
            st.session_state.datasets_page = page + 1
            st.rerun()
    
    # Display current page
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_datasets = datasets[start_idx:end_idx]
    
    # Prepare table data
    table_data = []
    for ds in page_datasets:
        table_data.append({
            "Name": ds.get("name", "N/A"),
            "Type": ds.get("dataset_type", "N/A").title(),
            "Row Count": format_number(ds.get("row_count")),
            "Upload Date": format_date(ds.get("upload_date") or ds.get("created_at")),
            "ID": ds.get("dataset_id") or ds.get("id", "N/A")
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download functionality
    st.markdown("---")
    st.subheader("Download Dataset")
    download_id = st.text_input("Enter Dataset ID to download", key="download_dataset_id")
    
    if st.button("Download", key="download_button"):
        if not download_id:
            st.warning("Please enter a dataset ID.")
        else:
            try:
                with loading_spinner.render_loading_container("Downloading dataset..."):
                    file_content = dataset_service.download_dataset(download_id)
                
                st.download_button(
                    label="📥 Download File",
                    data=file_content,
                    file_name=f"dataset_{download_id}.csv",
                    mime="text/csv"
                )
            except APIError as e:
                error_message.render_api_error(e)
            except Exception as e:
                error_message.render_error_message(e)
