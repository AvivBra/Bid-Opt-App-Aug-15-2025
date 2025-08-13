"""
Portfolio comparison and validation
"""

import pandas as pd
from typing import Dict, List, Tuple
from io import BytesIO


def compare_portfolios(
    bulk_portfolios: List[str], template_portfolios: List[str]
) -> Dict[str, List[str]]:
    """
    Compare portfolios between bulk and template

    Args:
        bulk_portfolios: List of portfolios from bulk file
        template_portfolios: List of portfolios from template

    Returns:
        Dictionary with 'missing' and 'excess' lists
    """
    bulk_set = set(bulk_portfolios)
    template_set = set(template_portfolios)

    missing = list(bulk_set - template_set)
    excess = list(template_set - bulk_set)

    return {"missing": sorted(missing), "excess": sorted(excess)}


def extract_template_portfolios(template_df: pd.DataFrame) -> Dict[str, dict]:
    """
    Extract portfolio data from template, excluding ignored ones

    Args:
        template_df: Template DataFrame

    Returns:
        Dictionary of portfolio data
    """
    portfolios = {}

    for _, row in template_df.iterrows():
        portfolio_name = row["Portfolio Name"]
        base_bid = row["Base Bid"]
        target_cpa = row.get("Target CPA", None)

        # Skip if marked as Ignore
        if str(base_bid).strip().lower() == "ignore":
            continue

        # Try to convert base_bid to float
        try:
            base_bid_float = float(base_bid)
        except (ValueError, TypeError):
            continue  # Skip invalid entries

        # Try to convert target_cpa if exists
        target_cpa_float = None
        if target_cpa and str(target_cpa).strip():
            try:
                target_cpa_float = float(target_cpa)
            except (ValueError, TypeError):
                pass  # Keep as None if invalid

        portfolios[portfolio_name] = {
            "base_bid": base_bid_float,
            "target_cpa": target_cpa_float,
        }

    return portfolios


def validate_template_structure(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate template file structure

    Args:
        df: Template DataFrame

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = ["Portfolio Name", "Base Bid", "Target CPA"]

    # Check if all required columns exist
    if list(df.columns) != required_columns:
        return False, "Template titles are incorrect"

    # Check if template has data
    if len(df) == 0:
        return False, "Template does not contain data"

    # Check if all portfolios are marked as Ignore
    non_ignored = 0
    for _, row in df.iterrows():
        if str(row["Base Bid"]).strip().lower() != "ignore":
            non_ignored += 1

    if non_ignored == 0:
        return (
            False,
            'All portfolios are marked as "Ignore". Cannot continue processing',
        )

    return True, ""


def create_portfolio_summary(missing: List[str], excess: List[str]) -> Dict[str, any]:
    """
    Create summary of portfolio comparison

    Args:
        missing: List of missing portfolios
        excess: List of excess portfolios

    Returns:
        Summary dictionary
    """
    return {
        "missing_count": len(missing),
        "excess_count": len(excess),
        "has_issues": len(missing) > 0 or len(excess) > 0,
        "can_continue": len(missing) == 0,
        "status": "ready" if len(missing) == 0 else "missing_portfolios",
    }
