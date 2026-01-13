"""File storage service for handling uploads and downloads."""

import os
import csv
import json
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile

from app.config import settings


ALLOWED_EXTENSIONS = {".csv", ".json", ".jsonl"}


def validate_file_type(filename: str) -> bool:
    """
    Validate file extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        True if valid, False otherwise
    """
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def save_uploaded_file(file: UploadFile, dataset_id: str) -> Tuple[str, int]:
    """
    Save uploaded file to storage.
    
    Args:
        file: Uploaded file object
        dataset_id: Dataset ID for filename
        
    Returns:
        Tuple of (file_path, row_count)
    """
    # Validate file type
    if not validate_file_type(file.filename):
        raise ValueError(f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Generate file path
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Create filename: {dataset_id}_{original_filename}
    file_ext = Path(file.filename).suffix
    filename = f"{dataset_id}_{file.filename}"
    file_path = upload_path / filename
    
    # Save file
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    # Count rows
    row_count = count_rows(file_path, file_ext)
    
    return str(file_path), row_count


def count_rows(file_path: Path, file_ext: str) -> int:
    """
    Count rows in uploaded file.
    
    Args:
        file_path: Path to the file
        file_ext: File extension
        
    Returns:
        Number of rows
    """
    try:
        if file_ext == ".csv":
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                return sum(1 for _ in reader) - 1  # Subtract header
        elif file_ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return len(data)
                elif isinstance(data, dict):
                    return 1
                return 0
        elif file_ext == ".jsonl":
            with open(file_path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        return 0
    except Exception:
        return 0


def read_file(file_path: str) -> bytes:
    """
    Read file for download.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File content as bytes
    """
    with open(file_path, "rb") as f:
        return f.read()


def delete_file(file_path: str) -> None:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file
    """
    if os.path.exists(file_path):
        os.remove(file_path)
