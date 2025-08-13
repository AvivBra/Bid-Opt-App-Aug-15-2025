"""
File writers for Excel files
"""

import pandas as pd
from io import BytesIO
from typing import Dict, Optional
from datetime import datetime


def create_excel(df: pd.DataFrame, sheet_name: str = "Sheet1") -> BytesIO:
    """
    Create Excel file from DataFrame

    Args:
        df: DataFrame to write
        sheet_name: Name for the sheet

    Returns:
        BytesIO buffer with Excel file
    """
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    buffer.seek(0)
    return buffer


def create_multi_sheet_excel(sheets_dict: Dict[str, pd.DataFrame]) -> BytesIO:
    """
    Create Excel file with multiple sheets

    Args:
        sheets_dict: Dictionary of sheet_name: DataFrame

    Returns:
        BytesIO buffer with Excel file
    """
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet_name, df in sheets_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    buffer.seek(0)
    return buffer


def create_template() -> BytesIO:
    """
    Create empty template file with required columns

    Returns:
        BytesIO buffer with template Excel file
    """
    df = pd.DataFrame(columns=["Portfolio Name", "Base Bid", "Target CPA"])
    return create_excel(df, sheet_name="Template")


def create_completion_template(missing_portfolios: list) -> BytesIO:
    """
    Create completion template with missing portfolios

    Args:
        missing_portfolios: List of portfolio names

    Returns:
        BytesIO buffer with completion template
    """
    df = pd.DataFrame(
        {
            "Portfolio Name": missing_portfolios,
            "Base Bid": [""] * len(missing_portfolios),
            "Target CPA": [""] * len(missing_portfolios),
        }
    )
    return create_excel(df, sheet_name="Completion")


def generate_filename(file_type: str) -> str:
    """
    Generate filename with timestamp

    Args:
        file_type: Type of file (Working File/Clean File)

    Returns:
        Formatted filename
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    return f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"
