"""
Initial cleanup for Bulk file data
"""

import pandas as pd
from typing import Dict


def initial_cleanup(bulk_df: pd.DataFrame, virtual_map_data: Dict[str, dict]) -> pd.DataFrame:
    """
    Perform initial cleanup on bulk data according to specifications
    
    Args:
        bulk_df: Raw bulk DataFrame
        virtual_map_data: Virtual map data dictionary
        
    Returns:
        Cleaned DataFrame
    """
    # Create a copy to avoid modifying original
    df = bulk_df.copy()
    
    # Filter 1: Entity must be "Product Targeting" or "Keyword"
    df = df[df['Entity'].isin(['Product Targeting', 'Keyword'])]
    
    # Filter 2: All state fields must be "enabled"
    df = df[df['State'] == 'enabled']
    df = df[df['Campaign State (Informational only)'] == 'enabled']
    df = df[df['Ad Group State (Informational only)'] == 'enabled']
    
    # Filter 3: Portfolio must exist in Virtual Map
    portfolio_names = set(virtual_map_data.keys())
    df = df[df['Portfolio Name (Informational only)'].isin(portfolio_names)]
    
    return df


def get_unique_portfolios(bulk_df: pd.DataFrame) -> list:
    """
    Get list of unique portfolio names from bulk file
    
    Args:
        bulk_df: Bulk DataFrame
        
    Returns:
        List of unique portfolio names
    """
    return bulk_df['Portfolio Name (Informational only)'].dropna().unique().tolist()


def count_rows_by_entity(df: pd.DataFrame) -> dict:
    """
    Count rows by entity type
    
    Args:
        df: DataFrame to count
        
    Returns:
        Dictionary with counts by entity
    """
    return df['Entity'].value_counts().to_dict()


def has_required_sheet(sheet_names: list, required_sheet: str = "Sponsored Products Campaigns") -> bool:
    """
    Check if required sheet exists
    
    Args:
        sheet_names: List of sheet names
        required_sheet: Name of required sheet
        
    Returns:
        True if sheet exists
    """
    return required_sheet in sheet_names