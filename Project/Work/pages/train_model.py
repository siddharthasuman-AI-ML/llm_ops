"""Train Model wizard page for configuring and launching training jobs."""

import streamlit as st
from services import experiment_service, model_service, dataset_service
from services.api_client import APIError
from components import loading_spinner, error_message
from utils.validators import (
    validate_required_field,
    validate_positive_number,
    validate_integer
)


def render():
    """Render the Train Model wizard page."""
    st.title("Train Model")
    st.markdown("Configure and launch a new training experiment.")
    
    # Initialize wizard state
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1
    
    if "wizard_data" not in st.session_state:
        st.session_state.wizard_data = {
            "name": "",
            "description": "",
            "goal": "",
            "base_model_id": None,
            "training_dataset_id": None,
            "eval_dataset_id": None,
            "learning_rate": None,
            "epochs": None,
            "batch_size": None
        }
    
    current_step = st.session_state.wizard_step
    
    # Progress indicator
    steps = [
        "Experiment Details",
        "Base Model",
        "Training Dataset",
        "Evaluation Dataset",
        "Training Config",
        "Review & Launch"
    ]
    
    progress = current_step / len(steps)
    st.progress(progress)
    st.caption(f"Step {current_step} of {len(steps)}: {steps[current_step - 1]}")
    
    st.markdown("---")
    
    # Step 1: Experiment Details
    if current_step == 1:
        render_step1()
    
    # Step 2: Base Model Selection
    elif current_step == 2:
        render_step2()
    
    # Step 3: Training Dataset Selection
    elif current_step == 3:
        render_step3()
    
    # Step 4: Evaluation Dataset Selection
    elif current_step == 4:
        render_step4()
    
    # Step 5: Training Configuration
    elif current_step == 5:
        render_step5()
    
    # Step 6: Review & Launch
    elif current_step == 6:
        render_step6()
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("◀ Previous", disabled=(current_step == 1), use_container_width=True):
            st.session_state.wizard_step = current_step - 1
            st.rerun()
    
    with col2:
        if st.button("Reset Wizard", use_container_width=True):
            st.session_state.wizard_step = 1
            st.session_state.wizard_data = {
                "name": "",
                "description": "",
                "goal": "",
                "base_model_id": None,
                "training_dataset_id": None,
                "eval_dataset_id": None,
                "learning_rate": None,
                "epochs": None,
                "batch_size": None
            }
            st.rerun()
    
    with col3:
        if current_step < 6:
            if st.button("Next ▶", use_container_width=True):
                # Validate current step before proceeding
                if validate_current_step(current_step):
                    st.session_state.wizard_step = current_step + 1
                    st.rerun()
                else:
                    st.error("Please fix the errors above before proceeding.")


def render_step1():
    """Render Step 1: Experiment Details."""
    st.subheader("Step 1: Experiment Details")
    
    name = st.text_input(
        "Experiment Name *",
        value=st.session_state.wizard_data["name"],
        placeholder="e.g., fine_tune_support_model_v1",
        key="wizard_name"
    )
    
    description = st.text_area(
        "Description",
        value=st.session_state.wizard_data["description"],
        placeholder="Optional description of this experiment",
        key="wizard_description"
    )
    
    goal = st.text_area(
        "Goal *",
        value=st.session_state.wizard_data["goal"],
        placeholder="What do you want to achieve with this experiment?",
        key="wizard_goal"
    )
    
    # Update session state
    st.session_state.wizard_data["name"] = name
    st.session_state.wizard_data["description"] = description
    st.session_state.wizard_data["goal"] = goal


def render_step2():
    """Render Step 2: Base Model Selection."""
    st.subheader("Step 2: Base Model Selection")
    
    try:
        with loading_spinner.render_loading_container("Loading base models..."):
            models = model_service.get_models(model_type="base")
    except APIError as e:
        error_message.render_api_error(e)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    if not models:
        st.warning("No base models available. Please upload a base model first.")
        return
    
    model_options = [f"{m.get('name', 'N/A')} ({m.get('id', 'N/A')[:8]})" for m in models]
    
    selected_model_idx = st.selectbox(
        "Select Base Model *",
        range(len(model_options)),
        format_func=lambda x: model_options[x],
        key="wizard_base_model"
    )
    
    if selected_model_idx is not None:
        selected_model = models[selected_model_idx]
        st.session_state.wizard_data["base_model_id"] = selected_model.get("id")
        
        # Show model details
        st.info(f"Selected: {selected_model.get('name')} - {selected_model.get('architecture', 'N/A')}")


def render_step3():
    """Render Step 3: Training Dataset Selection."""
    st.subheader("Step 3: Training Dataset Selection")
    
    try:
        with loading_spinner.render_loading_container("Loading training datasets..."):
            datasets = dataset_service.get_datasets()
            training_datasets = [d for d in datasets if d.get("dataset_type") == "training"]
    except APIError as e:
        error_message.render_api_error(e)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    if not training_datasets:
        st.warning("No training datasets available. Please upload a training dataset first.")
        return
    
    dataset_options = [f"{d.get('name', 'N/A')} ({d.get('id', 'N/A')[:8]})" for d in training_datasets]
    
    selected_dataset_idx = st.selectbox(
        "Select Training Dataset *",
        range(len(dataset_options)),
        format_func=lambda x: dataset_options[x],
        key="wizard_training_dataset"
    )
    
    if selected_dataset_idx is not None:
        selected_dataset = training_datasets[selected_dataset_idx]
        st.session_state.wizard_data["training_dataset_id"] = selected_dataset.get("id")
        
        # Show dataset details
        st.info(f"Selected: {selected_dataset.get('name')} - {selected_dataset.get('row_count', 'N/A')} rows")


def render_step4():
    """Render Step 4: Evaluation Dataset Selection."""
    st.subheader("Step 4: Evaluation Dataset Selection")
    
    try:
        with loading_spinner.render_loading_container("Loading evaluation datasets..."):
            datasets = dataset_service.get_datasets()
            eval_datasets = [d for d in datasets if d.get("dataset_type") == "evaluation"]
    except APIError as e:
        error_message.render_api_error(e)
        return
    except Exception as e:
        error_message.render_error_message(e)
        return
    
    # Evaluation dataset is optional
    eval_options = ["None (Skip Evaluation)"] + [f"{d.get('name', 'N/A')} ({d.get('id', 'N/A')[:8]})" for d in eval_datasets]
    
    selected_eval_idx = st.selectbox(
        "Select Evaluation Dataset (Optional)",
        range(len(eval_options)),
        format_func=lambda x: eval_options[x],
        key="wizard_eval_dataset"
    )
    
    if selected_eval_idx == 0:
        st.session_state.wizard_data["eval_dataset_id"] = None
    else:
        selected_dataset = eval_datasets[selected_eval_idx - 1]
        st.session_state.wizard_data["eval_dataset_id"] = selected_dataset.get("id")
        st.info(f"Selected: {selected_dataset.get('name')} - {selected_dataset.get('row_count', 'N/A')} rows")


def render_step5():
    """Render Step 5: Training Configuration."""
    st.subheader("Step 5: Training Configuration")
    
    learning_rate = st.number_input(
        "Learning Rate *",
        min_value=1e-6,
        max_value=1.0,
        value=st.session_state.wizard_data["learning_rate"] or 0.001,
        step=0.0001,
        format="%.6f",
        key="wizard_learning_rate"
    )
    
    epochs = st.number_input(
        "Epochs *",
        min_value=1,
        max_value=1000,
        value=st.session_state.wizard_data["epochs"] or 10,
        step=1,
        key="wizard_epochs"
    )
    
    batch_size = st.number_input(
        "Batch Size *",
        min_value=1,
        max_value=1024,
        value=st.session_state.wizard_data["batch_size"] or 32,
        step=1,
        key="wizard_batch_size"
    )
    
    # Update session state
    st.session_state.wizard_data["learning_rate"] = learning_rate
    st.session_state.wizard_data["epochs"] = int(epochs)
    st.session_state.wizard_data["batch_size"] = int(batch_size)


def render_step6():
    """Render Step 6: Review & Launch."""
    st.subheader("Step 6: Review & Launch")
    
    data = st.session_state.wizard_data
    
    # Summary
    st.markdown("### Experiment Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {data['name']}")
        st.markdown(f"**Description:** {data['description'] or 'N/A'}")
        st.markdown(f"**Goal:** {data['goal']}")
    
    with col2:
        st.markdown(f"**Base Model ID:** {data['base_model_id'][:8] + '...' if data['base_model_id'] else 'N/A'}")
        st.markdown(f"**Training Dataset ID:** {data['training_dataset_id'][:8] + '...' if data['training_dataset_id'] else 'N/A'}")
        st.markdown(f"**Eval Dataset ID:** {data['eval_dataset_id'][:8] + '...' if data['eval_dataset_id'] else 'None'}")
    
    st.markdown("---")
    st.markdown("### Training Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Learning Rate", data['learning_rate'])
    
    with col2:
        st.metric("Epochs", data['epochs'])
    
    with col3:
        st.metric("Batch Size", data['batch_size'])
    
    st.markdown("---")
    
    # Launch button
    if st.button("🚀 Launch Experiment", type="primary", use_container_width=True):
        # Final validation
        if validate_all_steps():
            try:
                with loading_spinner.render_loading_container("Creating experiment..."):
                    result = experiment_service.create_experiment(
                        name=data["name"],
                        description=data["description"],
                        goal=data["goal"],
                        base_model_id=data["base_model_id"],
                        training_dataset_id=data["training_dataset_id"],
                        eval_dataset_id=data["eval_dataset_id"],
                        learning_rate=data["learning_rate"],
                        epochs=data["epochs"],
                        batch_size=data["batch_size"]
                    )
                
                st.success(f"✅ Experiment '{result.get('name', data['name'])}' created successfully!")
                st.balloons()
                
                # Reset wizard
                st.session_state.wizard_step = 1
                st.session_state.wizard_data = {
                    "name": "",
                    "description": "",
                    "goal": "",
                    "base_model_id": None,
                    "training_dataset_id": None,
                "eval_dataset_id": None,
                    "learning_rate": None,
                    "epochs": None,
                    "batch_size": None
                }
                
                # Option to navigate to experiments page
                if st.button("View Experiment", use_container_width=True):
                    st.session_state.current_page = "experiments"
                    st.rerun()
                
            except APIError as e:
                error_message.render_api_error(e)
            except Exception as e:
                error_message.render_error_message(e)
        else:
            st.error("Please fix all errors before launching.")


def validate_current_step(step: int) -> bool:
    """Validate the current wizard step."""
    data = st.session_state.wizard_data
    
    if step == 1:
        name_valid, _ = validate_required_field(data["name"], "Experiment name")
        goal_valid, _ = validate_required_field(data["goal"], "Goal")
        return name_valid and goal_valid
    
    elif step == 2:
        return data["base_model_id"] is not None
    
    elif step == 3:
        return data["training_dataset_id"] is not None
    
    elif step == 4:
        return True  # Eval dataset is optional
    
    elif step == 5:
        lr_valid, _ = validate_positive_number(data["learning_rate"], "Learning rate")
        epochs_valid, _ = validate_integer(data["epochs"], "Epochs", min_value=1)
        batch_valid, _ = validate_integer(data["batch_size"], "Batch size", min_value=1)
        return lr_valid and epochs_valid and batch_valid
    
    return True


def validate_all_steps() -> bool:
    """Validate all wizard steps."""
    for step in range(1, 7):
        if not validate_current_step(step):
            return False
    return True
