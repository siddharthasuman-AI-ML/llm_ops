"""Evaluations page for analyzing model performance."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from services import evaluation_service, experiment_service, model_service, dataset_service
from services.api_client import APIError
from components import loading_spinner, error_message, empty_state
from utils.formatters import format_date


def render():
    """Render the Evaluations page."""
    st.title("Evaluations")
    st.markdown("Analyze model performance and view evaluation metrics.")
    
    # Load data for selectors
    try:
        with loading_spinner.render_loading_container("Loading data..."):
            experiments = experiment_service.get_experiments()
            models = model_service.get_models()
            datasets = dataset_service.get_datasets()
            evaluations = evaluation_service.get_evaluations()
    except APIError as e:
        error_message.render_api_error(e, show_retry=True, retry_callback=render)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    # Evaluation selector
    st.subheader("Select Evaluation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        experiment_options = ["All"] + [f"{exp.get('name', 'N/A')} ({exp.get('id', 'N/A')[:8]})" for exp in experiments]
        selected_experiment = st.selectbox("Experiment", experiment_options, key="eval_experiment")
    
    with col2:
        model_options = ["All"] + [f"{m.get('name', 'N/A')} ({m.get('id', 'N/A')[:8]})" for m in models]
        selected_model = st.selectbox("Model", model_options, key="eval_model")
    
    with col3:
        dataset_options = ["All"] + [f"{d.get('name', 'N/A')} ({d.get('id', 'N/A')[:8]})" for d in datasets]
        selected_dataset = st.selectbox("Evaluation Dataset", dataset_options, key="eval_dataset")
    
    # Filter evaluations
    filtered_evaluations = evaluations
    
    if selected_experiment != "All":
        exp_id = experiments[experiment_options.index(selected_experiment) - 1].get("id")
        filtered_evaluations = [e for e in filtered_evaluations if e.get("experiment_id") == exp_id]
    
    if not filtered_evaluations:
        empty_state.render_empty_state(
            "No evaluations found matching the selected criteria.",
            icon="📊"
        )
        return
    
    # Evaluation selector
    eval_options = [f"Evaluation {i+1} ({e.get('id', 'N/A')[:8]})" for i, e in enumerate(filtered_evaluations)]
    selected_eval_idx = st.selectbox("Select Evaluation", range(len(eval_options)), format_func=lambda x: eval_options[x], key="selected_eval")
    
    selected_evaluation = filtered_evaluations[selected_eval_idx]
    
    # Load full evaluation details
    eval_id = selected_evaluation.get("id")
    if not eval_id:
        st.warning("Selected evaluation has no ID.")
        return
    
    try:
        with loading_spinner.render_loading_container("Loading evaluation details..."):
            eval_details = evaluation_service.get_evaluation(eval_id)
    except APIError as e:
        error_message.render_api_error(e)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    st.markdown("---")
    
    # Metrics panel
    st.subheader("Metrics")
    
    metrics = eval_details.get("metrics", {})
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            accuracy = metrics.get("accuracy")
            if accuracy is not None:
                st.metric("Accuracy", f"{accuracy:.4f}" if isinstance(accuracy, float) else accuracy)
        
        with col2:
            f1 = metrics.get("f1")
            if f1 is not None:
                st.metric("F1 Score", f"{f1:.4f}" if isinstance(f1, float) else f1)
        
        with col3:
            perplexity = metrics.get("perplexity")
            if perplexity is not None:
                st.metric("Perplexity", f"{perplexity:.4f}" if isinstance(perplexity, float) else perplexity)
        
        with col4:
            st.metric("Created", format_date(eval_details.get("created_at")))
        
        # Show all metrics as JSON if there are more
        if len(metrics) > 3:
            with st.expander("View All Metrics"):
                st.json(metrics)
    else:
        st.info("No metrics available for this evaluation.")
    
    # Loss curve visualization
    st.markdown("---")
    st.subheader("Loss Curve")
    
    loss_curve = eval_details.get("loss_curve")
    if loss_curve:
        if isinstance(loss_curve, dict):
            # Extract data
            epochs = loss_curve.get("epochs", [])
            train_loss = loss_curve.get("train_loss", [])
            val_loss = loss_curve.get("val_loss", [])
            
            if epochs and (train_loss or val_loss):
                fig = go.Figure()
                
                if train_loss:
                    fig.add_trace(go.Scatter(
                        x=epochs if epochs else list(range(len(train_loss))),
                        y=train_loss,
                        mode='lines+markers',
                        name='Training Loss',
                        line=dict(color='blue')
                    ))
                
                if val_loss:
                    fig.add_trace(go.Scatter(
                        x=epochs if epochs else list(range(len(val_loss))),
                        y=val_loss,
                        mode='lines+markers',
                        name='Validation Loss',
                        line=dict(color='red')
                    ))
                
                fig.update_layout(
                    title="Training and Validation Loss",
                    xaxis_title="Epoch",
                    yaxis_title="Loss",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Loss curve data is incomplete.")
        elif isinstance(loss_curve, list):
            # Simple list of loss values
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(loss_curve))),
                y=loss_curve,
                mode='lines+markers',
                name='Loss',
                line=dict(color='blue')
            ))
            fig.update_layout(
                title="Loss Curve",
                xaxis_title="Step",
                yaxis_title="Loss"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.json(loss_curve)
    else:
        st.info("No loss curve data available.")
    
    # Training statistics table
    st.markdown("---")
    st.subheader("Training Statistics")
    
    training_stats = eval_details.get("training_statistics")
    if training_stats:
        if isinstance(training_stats, dict):
            # Convert to table
            stats_data = []
            for key, value in training_stats.items():
                stats_data.append({
                    "Metric": key.replace("_", " ").title(),
                    "Value": value
                })
            
            df = pd.DataFrame(stats_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.json(training_stats)
    else:
        st.info("No training statistics available.")
    
    # Compare evaluations
    st.markdown("---")
    st.subheader("Compare Evaluations")
    
    if len(filtered_evaluations) > 1:
        compare_options = [f"Evaluation {i+1} ({e.get('id', 'N/A')[:8]})" for i, e in enumerate(filtered_evaluations)]
        selected_compare = st.multiselect("Select evaluations to compare", compare_options, key="compare_evals")
        
        if selected_compare:
            compare_data = []
            for option in selected_compare:
                idx = compare_options.index(option)
                eval_data = filtered_evaluations[idx]
                metrics = eval_data.get("metrics", {})
                compare_data.append({
                    "Evaluation": option,
                    "Accuracy": metrics.get("accuracy", "N/A"),
                    "F1": metrics.get("f1", "N/A"),
                    "Perplexity": metrics.get("perplexity", "N/A")
                })
            
            compare_df = pd.DataFrame(compare_data)
            st.dataframe(compare_df, use_container_width=True, hide_index=True)
