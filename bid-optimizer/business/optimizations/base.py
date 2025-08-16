"""
Base Optimization Class
Abstract base class for all optimization implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
from datetime import datetime


class BaseOptimization(ABC):
    """Abstract base class for all optimizations"""

    # Class attributes to be overridden by subclasses
    name: str = "Base Optimization"
    description: str = "Base optimization class"
    required_columns: List[str] = []

    def __init__(self):
        """Initialize optimization"""
        self.stats = {
            "start_time": None,
            "end_time": None,
            "rows_processed": 0,
            "rows_modified": 0,
            "rows_with_errors": 0,
            "error_messages": [],
            "warning_messages": [],
        }
        self.pink_highlighted_rows = []

    @abstractmethod
    def validate_inputs(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> Tuple[bool, List[str]]:
        """
        Validate that all required data is present

        Args:
            bulk_df: Cleaned bulk DataFrame
            template_df: Template DataFrame

        Returns:
            Tuple of (is_valid, error_messages)
        """
        pass

    @abstractmethod
    def apply_optimization(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        Apply the optimization logic

        Args:
            bulk_df: Cleaned bulk DataFrame
            template_df: Template DataFrame with portfolio settings

        Returns:
            Dictionary with sheet names as keys and DataFrames as values
            Can return multiple sheets for complex optimizations
        """
        pass

    def optimize(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Main optimization method - orchestrates the process

        Args:
            bulk_df: Cleaned bulk DataFrame
            template_df: Template DataFrame

        Returns:
            Tuple of (optimized_data, stats)
        """
        self.stats["start_time"] = datetime.now()
        self.stats["rows_processed"] = len(bulk_df)

        # Validate inputs
        is_valid, errors = self.validate_inputs(bulk_df, template_df)
        if not is_valid:
            self.stats["error_messages"] = errors
            self.stats["end_time"] = datetime.now()
            # Return original data unchanged if validation fails
            return {"Clean": bulk_df.copy()}, self.stats

        # Apply optimization
        try:
            optimized_sheets = self.apply_optimization(bulk_df, template_df)

            # Ensure all sheets have Operation = "Update"
            for sheet_name, df in optimized_sheets.items():
                if "Operation" in df.columns:
                    df["Operation"] = "Update"

            self.stats["end_time"] = datetime.now()
            self.stats["duration"] = (
                self.stats["end_time"] - self.stats["start_time"]
            ).total_seconds()

            return optimized_sheets, self.stats

        except Exception as e:
            self.stats["error_messages"].append(f"Optimization failed: {str(e)}")
            self.stats["end_time"] = datetime.now()
            # Return original data on error
            return {"Clean": bulk_df.copy()}, self.stats

    def check_bid_limits(
        self, df: pd.DataFrame, bid_column: str = "Bid"
    ) -> Tuple[int, int, int]:
        """
        Check for bid values outside allowed range

        Args:
            df: DataFrame to check
            bid_column: Name of bid column

        Returns:
            Tuple of (below_min, above_max, errors)
        """
        if bid_column not in df.columns:
            return 0, 0, 0

        MIN_BID = 0.02
        MAX_BID = 1.25

        # Convert to numeric, handling errors
        bid_values = pd.to_numeric(df[bid_column], errors="coerce")

        below_min = (bid_values < MIN_BID).sum()
        above_max = (bid_values > MAX_BID).sum()
        errors = bid_values.isna().sum()

        # Mark rows for pink highlighting
        problem_indices = df[
            (bid_values < MIN_BID) | (bid_values > MAX_BID) | (bid_values.isna())
        ].index.tolist()

        self.pink_highlighted_rows.extend(problem_indices)

        return below_min, above_max, errors

    def add_helper_columns(
        self,
        df: pd.DataFrame,
        helper_columns: Dict[str, Any],
        insert_position: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Add helper columns to DataFrame

        Args:
            df: DataFrame to modify
            helper_columns: Dictionary of column_name: values
            insert_position: Position to insert columns (default: before 'Bid')

        Returns:
            DataFrame with helper columns added
        """
        df_copy = df.copy()

        # Find insert position (left of Bid column)
        if insert_position is None:
            if "Bid" in df_copy.columns:
                insert_position = df_copy.columns.get_loc("Bid")
            else:
                insert_position = len(df_copy.columns)

        # Add helper columns
        for i, (col_name, col_values) in enumerate(helper_columns.items()):
            df_copy.insert(insert_position + i, col_name, col_values)

        return df_copy

    def get_portfolio_value(
        self,
        portfolio_name: str,
        template_df: pd.DataFrame,
        column: str,
        default: Any = None,
    ) -> Any:
        """
        Get value from template for a specific portfolio

        Args:
            portfolio_name: Name of portfolio
            template_df: Template DataFrame
            column: Column to retrieve
            default: Default value if not found

        Returns:
            Value from template or default
        """
        if portfolio_name in template_df["Portfolio Name"].values:
            row = template_df[template_df["Portfolio Name"] == portfolio_name]
            if not row.empty and column in row.columns:
                value = row.iloc[0][column]
                # Handle NaN values
                if pd.isna(value):
                    return default
                return value
        return default

    def generate_summary_message(self) -> str:
        """
        Generate summary message for user

        Returns:
            Formatted summary message
        """
        messages = []

        if self.stats["rows_modified"] > 0:
            messages.append(
                f"Applied {self.name} optimization to {self.stats['rows_modified']} rows"
            )

        # Add bid limit warnings if any
        if hasattr(self, "bid_check_results"):
            below, above, errors = self.bid_check_results
            if below > 0 or above > 0 or errors > 0:
                messages.append(
                    f"{below} rows below 0.02, {above} rows above 1.25, "
                    f"{errors} rows with calculation errors"
                )

        # Add any warning messages
        for warning in self.stats["warning_messages"]:
            messages.append(warning)

        return " | ".join(messages) if messages else f"{self.name} completed"
