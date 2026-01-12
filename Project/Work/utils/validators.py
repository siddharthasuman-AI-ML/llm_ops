"""Form validation helpers for the SLM Training Platform UI."""

import os
from typing import Optional, Tuple


ALLOWED_FILE_EXTENSIONS = {".csv", ".json", ".jsonl"}
ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/json",
    "text/plain"  # JSONL files may be detected as text/plain
}


def validate_required_field(value: Optional[str], field_name: str) -> Tuple[bool, str]:
    """
    Validate that a required field is not empty.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error message
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not value or not value.strip():
        return False, f"{field_name} is required."
    return True, ""


def validate_file_type(uploaded_file) -> Tuple[bool, str]:
    """
    Validate that uploaded file is of allowed type.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "Please select a file to upload."
    
    # Get file extension
    file_name = uploaded_file.name.lower()
    file_ext = os.path.splitext(file_name)[1]
    
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        allowed = ", ".join(ALLOWED_FILE_EXTENSIONS)
        return False, f"Invalid file type. Allowed types: {allowed}"
    
    return True, ""


def validate_positive_number(value: Optional[float], field_name: str) -> Tuple[bool, str]:
    """
    Validate that a number is positive.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error message
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if value is None:
        return False, f"{field_name} is required."
    
    try:
        num_value = float(value)
        if num_value <= 0:
            return False, f"{field_name} must be a positive number."
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number."


def validate_integer(value: Optional[int], field_name: str, min_value: Optional[int] = None) -> Tuple[bool, str]:
    """
    Validate that a value is a valid integer.
    
    Args:
        value: The value to validate
        field_name: Name of the field for error message
        min_value: Optional minimum value
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if value is None:
        return False, f"{field_name} is required."
    
    try:
        int_value = int(value)
        if min_value is not None and int_value < min_value:
            return False, f"{field_name} must be at least {min_value}."
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid integer."


def validate_dataset_type(dataset_type: Optional[str]) -> Tuple[bool, str]:
    """
    Validate dataset type is either 'training' or 'evaluation'.
    
    Args:
        dataset_type: The dataset type to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not dataset_type:
        return False, "Dataset type is required."
    
    if dataset_type not in ["training", "evaluation"]:
        return False, "Dataset type must be either 'training' or 'evaluation'."
    
    return True, ""
