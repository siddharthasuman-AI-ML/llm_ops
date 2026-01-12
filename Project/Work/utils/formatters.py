"""Data formatting helpers for the SLM Training Platform UI."""

from datetime import datetime
from typing import Optional


def format_date(date_str: Optional[str]) -> str:
    """
    Format a date string to a readable format.
    
    Args:
        date_str: ISO format date string
        
    Returns:
        Formatted date string or "N/A" if invalid
    """
    if not date_str:
        return "N/A"
    
    try:
        # Try parsing ISO format
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        try:
            # Try parsing other common formats
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            return date_str  # Return as-is if can't parse


def format_number(num: Optional[int]) -> str:
    """
    Format a number with thousand separators.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted number string or "N/A" if invalid
    """
    if num is None:
        return "N/A"
    
    try:
        return f"{num:,}"
    except (ValueError, TypeError):
        return str(num)


def format_file_size(size_bytes: Optional[int]) -> str:
    """
    Format file size in bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes is None:
        return "N/A"
    
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} TB"


def truncate_text(text: Optional[str], max_length: int = 50) -> str:
    """
    Truncate text to a maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."
