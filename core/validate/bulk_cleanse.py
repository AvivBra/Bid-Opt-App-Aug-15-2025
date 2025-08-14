"""
Initial cleanup for Bulk file data
"""

import pandas as pd
from typing import List, Optional


def initial_cleanup(
    bulk_df: pd.DataFrame, ignored_portfolios: List[str] = None
) -> pd.DataFrame:
    """
    Perform initial cleanup on bulk data according to specifications

    Args:
        bulk_df: Raw bulk DataFrame
        ignored_portfolios: List of portfolios to ignore (from Virtual Map)

    Returns:
        Cleaned DataFrame
    """
    # Create a copy to avoid modifying original
    df = bulk_df.copy()

    # Filter 1: Entity must be "Product Targeting" or "Keyword"
    df = df[df["Entity"].isin(["Product Targeting", "Keyword"])]

    # Filter 2: All state fields must be "enabled"
    df = df[df["State"] == "enabled"]
    df = df[df["Campaign State (Informational only)"] == "enabled"]
    df = df[df["Ad Group State (Informational only)"] == "enabled"]

    # Filter 3: Remove rows with ignored portfolios
    if ignored_portfolios:
        df = df[~df["Portfolio Name (Informational only)"].isin(ignored_portfolios)]

    return df


def get_unique_portfolios(df: pd.DataFrame) -> List[str]:
    """
    Get list of unique portfolio names from DataFrame

    Args:
        df: DataFrame (bulk or cleaned)

    Returns:
        List of unique portfolio names
    """
    if "Portfolio Name (Informational only)" in df.columns:
        return df["Portfolio Name (Informational only)"].dropna().unique().tolist()
    return []


def count_rows_by_entity(df: pd.DataFrame) -> dict:
    """
    Count rows by entity type

    Args:
        df: DataFrame to count

    Returns:
        Dictionary with counts by entity
    """
    if "Entity" in df.columns:
        return df["Entity"].value_counts().to_dict()
    return {}


def has_required_sheet(
    sheet_names: list, required_sheet: str = "Sponsored Products Campaigns"
) -> bool:
    """
    Check if required sheet exists

    Args:
        sheet_names: List of sheet names
        required_sheet: Name of required sheet

    Returns:
        True if sheet exists
    """
    return required_sheet in sheet_names


def validate_cleanup_result(df: pd.DataFrame) -> bool:
    """
    Check if cleanup resulted in valid data

    Args:
        df: Cleaned DataFrame

    Returns:
        True if data is valid (has rows)
    """
    return len(df) > 0
