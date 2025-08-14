"""
File readers for Excel and CSV files
"""

import pandas as pd
from io import BytesIO
from typing import Optional, List
from config.constants import (
    BULK_REQUIRED_COLUMNS,
    TEMPLATE_REQUIRED_COLUMNS,
    SPONSORED_PRODUCTS_SHEET,
    MAX_FILE_SIZE_BYTES,
)


def read_excel(file: BytesIO, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Read Excel file and return DataFrame

    Args:
        file: Excel file as BytesIO
        sheet_name: Name of sheet to read (optional)

    Returns:
        DataFrame with file contents
    """
    # Read with specific dtypes to prevent scientific notation for IDs
    dtype_spec = {
        "Campaign ID": str,
        "Ad Group ID": str,
        "Portfolio ID": str,
        "Ad ID": str,
        "Keyword ID": str,
        "Product Targeting ID": str,
    }

    if sheet_name:
        df = pd.read_excel(
            file, sheet_name=sheet_name, dtype=dtype_spec, engine="openpyxl"
        )
    else:
        df = pd.read_excel(file, dtype=dtype_spec, engine="openpyxl")

    return df


def read_csv(file: BytesIO) -> pd.DataFrame:
    """
    Read CSV file and return DataFrame

    Args:
        file: CSV file as BytesIO

    Returns:
        DataFrame with file contents
    """
    # Read with specific dtypes to prevent scientific notation for IDs
    dtype_spec = {
        "Campaign ID": str,
        "Ad Group ID": str,
        "Portfolio ID": str,
        "Ad ID": str,
        "Keyword ID": str,
        "Product Targeting ID": str,
    }

    df = pd.read_csv(file, dtype=dtype_spec)
    return df


def validate_headers(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that DataFrame has all required columns

    Args:
        df: DataFrame to validate
        required_columns: List of required column names

    Returns:
        True if all columns present, False otherwise
    """
    df_columns = list(df.columns)
    return df_columns == required_columns


def get_sheet_names(file: BytesIO) -> List[str]:
    """
    Get list of sheet names from Excel file

    Args:
        file: Excel file as BytesIO

    Returns:
        List of sheet names
    """
    excel_file = pd.ExcelFile(file, engine="openpyxl")
    return excel_file.sheet_names


def check_sheet_exists(file: BytesIO, sheet_name: str) -> bool:
    """
    Check if specific sheet exists in Excel file

    Args:
        file: Excel file as BytesIO
        sheet_name: Name of sheet to check

    Returns:
        True if sheet exists, False otherwise
    """
    sheets = get_sheet_names(file)
    return sheet_name in sheets


def read_bulk_file(file: BytesIO) -> Optional[pd.DataFrame]:
    """
    Read Bulk file from Sponsored Products Campaigns sheet

    Args:
        file: Bulk file as BytesIO

    Returns:
        DataFrame or None if error
    """
    try:
        # Check file size
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)

        if size > MAX_FILE_SIZE_BYTES:
            return None

        # Check if required sheet exists
        if check_sheet_exists(file, SPONSORED_PRODUCTS_SHEET):
            df = read_excel(file, sheet_name=SPONSORED_PRODUCTS_SHEET)
        else:
            # Try as CSV
            df = read_csv(file)

        # Validate headers
        if validate_headers(df, BULK_REQUIRED_COLUMNS):
            return df
        else:
            return None

    except Exception:
        return None


def read_template_file(file: BytesIO) -> Optional[pd.DataFrame]:
    """
    Read Template file (Excel or CSV)

    Args:
        file: Template file as BytesIO

    Returns:
        DataFrame or None if error
    """
    try:
        # Check file size
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)

        if size > MAX_FILE_SIZE_BYTES:
            return None

        # Try to read as Excel first
        try:
            df = read_excel(file)
        except:
            # Try as CSV if Excel fails
            file.seek(0)
            df = read_csv(file)

        # Validate headers
        if not validate_headers(df, TEMPLATE_REQUIRED_COLUMNS):
            return None

        # Check if template is empty (only headers)
        if len(df) == 0:
            return None

        return df

    except Exception:
        return None
