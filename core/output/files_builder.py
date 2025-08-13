"""
Output file generation for Working and Clean files
"""

import pandas as pd
from io import BytesIO
from typing import Dict, List
from datetime import datetime


def create_working_file(
    bulk_df: pd.DataFrame, optimization_types: List[str]
) -> BytesIO:
    """
    Create Working File with Clean and Working sheets

    Args:
        bulk_df: Original bulk DataFrame
        optimization_types: List of selected optimization types

    Returns:
        BytesIO buffer with Working File
    """
    # For mockup, just copy the data and set Operation to Update
    df_copy = bulk_df.copy()
    if "Operation" in df_copy.columns:
        df_copy["Operation"] = "Update"

    # Create sheets dictionary
    sheets = {}

    # For mockup, only Zero Sales is implemented
    if "Zero Sales" in optimization_types:
        sheets["Clean Zero Sales"] = df_copy
        sheets["Working Zero Sales"] = df_copy.copy()  # Same data for mockup

    # Create Excel file with multiple sheets
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    buffer.seek(0)
    return buffer


def create_clean_file(bulk_df: pd.DataFrame, optimization_types: List[str]) -> BytesIO:
    """
    Create Clean File with only Clean sheets

    Args:
        bulk_df: Original bulk DataFrame
        optimization_types: List of selected optimization types

    Returns:
        BytesIO buffer with Clean File
    """
    # For mockup, just copy the data and set Operation to Update
    df_copy = bulk_df.copy()
    if "Operation" in df_copy.columns:
        df_copy["Operation"] = "Update"

    # Create sheets dictionary
    sheets = {}

    # For mockup, only Zero Sales is implemented
    if "Zero Sales" in optimization_types:
        sheets["Clean Zero Sales"] = df_copy

    # Create Excel file
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    buffer.seek(0)
    return buffer


def format_excel_columns(writer, sheet_name: str, df: pd.DataFrame):
    """
    Apply formatting to Excel columns

    Args:
        writer: ExcelWriter object
        sheet_name: Name of the sheet
        df: DataFrame being written
    """
    worksheet = writer.sheets[sheet_name]

    # Set column widths
    for idx, col in enumerate(df.columns):
        column_letter = chr(65 + idx)  # A, B, C, etc.
        if idx < 26:  # Handle up to Z column
            worksheet.column_dimensions[column_letter].width = 15

    # Center align all cells
    from openpyxl.styles import Alignment

    for row in worksheet.iter_rows(min_row=2, max_row=len(df) + 1):
        for cell in row:
            cell.alignment = Alignment(horizontal="center")


def generate_output_filename(file_type: str) -> str:
    """
    Generate filename for output files

    Args:
        file_type: Type of file (Working File or Clean File)

    Returns:
        Formatted filename
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    return f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"


def create_mock_statistics() -> Dict[str, any]:
    """
    Create mock statistics for output display

    Returns:
        Dictionary with mock statistics
    """
    return {
        "total_rows": 1234,
        "optimizations_applied": 856,
        "average_bid_change": "+15%",
        "processing_time": "2.3s",
        "calculation_errors": 7,
        "high_bids": 3,
        "low_bids": 2,
    }
