"""
Filename Generator
Generates dynamic filenames with current date and time
"""

from datetime import datetime
from typing import Optional


def generate_output_filename(
    file_type: str, timestamp: Optional[datetime] = None
) -> str:
    """
    Generate filename with current date and time

    Args:
        file_type: 'Working' or 'Clean'
        timestamp: Optional specific timestamp (defaults to now)

    Returns:
        Formatted filename string
        Example: "Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx"
    """
    if timestamp is None:
        timestamp = datetime.now()

    # Format date and time
    date_str = timestamp.strftime("%Y-%m-%d")
    time_str = timestamp.strftime("%H-%M")

    # Create filename
    filename = f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"

    return filename


def get_sheet_name(optimization_name: str, sheet_type: str) -> str:
    """
    Generate sheet name for optimization

    Args:
        optimization_name: Name of optimization (e.g., "Zero Sales")
        sheet_type: 'Clean' or 'Working'

    Returns:
        Sheet name (e.g., "Clean Zero Sales")
    """
    return f"{sheet_type} {optimization_name}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for all operating systems
    """
    # Replace invalid characters
    invalid_chars = ["<", ">", ":", '"', "/", "\\", "?", "*"]

    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, "-")

    return sanitized


def get_file_size_display(size_bytes: int) -> str:
    """
    Convert file size to human-readable format

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string (e.g., "2.4 MB", "125 KB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        size_kb = size_bytes / 1024
        return f"{size_kb:.1f} KB"
    else:
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f} MB"
