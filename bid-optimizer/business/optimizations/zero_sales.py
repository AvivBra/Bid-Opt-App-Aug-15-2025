"""
Zero Sales Optimization
Reduces bids for keywords/products with no sales (Units = 0)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from .base import BaseOptimization


class ZeroSalesOptimization(BaseOptimization):
    """Zero Sales optimization implementation"""

    name = "Zero Sales"
    description = "Reduces bids for keywords and products with no unit sales"
    required_columns = [
        "Entity",
        "Units",
        "Portfolio Name (Informational only)",
        "Campaign ID",
        "Campaign Name (Informational only)",
        "Bid",
        "Clicks",
        "Percentage",
    ]

    # Flat portfolio patterns to exclude
    FLAT_PORTFOLIOS = [
        "Flat 30",
        "Flat 25",
        "Flat 40",
        "Flat 25 | Opt",
        "Flat 30 | Opt",
        "Flat 20",
        "Flat 15",
        "Flat 40 | Opt",
        "Flat 20 | Opt",
        "Flat 15 | Opt",
    ]

    def validate_inputs(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> Tuple[bool, List[str]]:
        """Validate required columns exist"""
        errors = []

        # Check bulk columns
        for col in self.required_columns:
            if col not in bulk_df.columns:
                errors.append(f"Required column '{col}' not found in Bulk file")

        # Check template columns
        template_required = ["Portfolio Name", "Base Bid", "Target CPA"]
        for col in template_required:
            if col not in template_df.columns:
                errors.append(f"Required column '{col}' not found in Template file")

        return len(errors) == 0, errors

    def apply_optimization(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """Apply Zero Sales optimization logic"""

        print(f"DEBUG: Starting with {len(bulk_df)} total rows")
        print(
            f"DEBUG: Unique Entity values: {bulk_df['Entity'].unique() if 'Entity' in bulk_df.columns else 'No Entity column'}"
        )

        # Step 1: Separate Bidding Adjustment FIRST (ALL of them, not filtered)
        bidding_adj_df = bulk_df[bulk_df["Entity"] == "Bidding Adjustment"].copy()
        main_data_df = bulk_df[bulk_df["Entity"] != "Bidding Adjustment"].copy()

        print(f"DEBUG: Found {len(bidding_adj_df)} Bidding Adjustment rows")
        print(f"DEBUG: Found {len(main_data_df)} non-Bidding Adjustment rows")

        # Check if Bidding Adjustment rows exist
        if len(bidding_adj_df) == 0:
            self.stats["warning_messages"].append(
                "Note: No Bidding Adjustment rows found"
            )

        # Step 2: Filter main data - Units = 0 and not Flat portfolio
        filtered_df = self._filter_data(main_data_df)

        print(f"DEBUG: After filtering Units=0: {len(filtered_df)} rows")

        if len(filtered_df) == 0:
            self.stats["warning_messages"].append(
                "No rows found with Units=0 after filtering"
            )
            # Still return Bidding Adjustment if exists
            result = {"Clean Zero Sales": bulk_df.copy()}
            if len(bidding_adj_df) > 0:
                result["Bidding Adjustment Zero Sales"] = bidding_adj_df
            return result

        # Step 3: Add helper columns (only to filtered main sheet)
        print(f"DEBUG: Total columns before helper: {len(filtered_df.columns)}")
        print(f"DEBUG: Bid column exists: {'Bid' in filtered_df.columns}")
        filtered_df = self._add_helper_columns(filtered_df, bidding_adj_df, template_df)
        print(f"DEBUG: Total columns after helper: {len(filtered_df.columns)}")

        # Check for helper columns
        helper_cols = [
            "Max BA",
            "Base Bid",
            "Target CPA",
            "Adj. CPA",
            "Old Bid",
            "calc1",
            "calc2",
        ]
        for col in helper_cols:
            if col in filtered_df.columns:
                print(f"DEBUG: Helper column '{col}' added successfully")
                # Show sample values
                sample_values = filtered_df[col].head(3).tolist()
                print(f"  Sample values: {sample_values}")

        # Step 4: Calculate new bids
        filtered_df = self._calculate_bids(filtered_df)

        # Step 5: Check bid limits and highlight errors
        below, above, errors = self.check_bid_limits(filtered_df)
        if below > 0 or above > 0 or errors > 0:
            self.bid_check_results = (below, above, errors)
            self.stats["warning_messages"].append(
                f"{below} rows below 0.02, {above} rows above 1.25, "
                f"{errors} rows with calculation errors"
            )

        # Set Operation = Update for all rows
        filtered_df["Operation"] = "Update"
        if len(bidding_adj_df) > 0:
            bidding_adj_df["Operation"] = "Update"

        # Update stats
        self.stats["rows_modified"] = len(filtered_df)

        # Return sheets - make sure helper columns are included
        result = {
            "Clean Zero Sales": filtered_df.copy(),  # Include all columns with helper columns
            "Working Zero Sales": filtered_df.copy(),  # Include all columns with helper columns
        }

        # Add Bidding Adjustment sheet if it has data
        if len(bidding_adj_df) > 0:
            print(
                f"DEBUG: Adding Bidding Adjustment sheet with {len(bidding_adj_df)} rows"
            )
            result["Bidding Adjustment Zero Sales"] = bidding_adj_df

        print(f"DEBUG: Returning {len(result)} sheets: {list(result.keys())}")

        return result

    def _filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 2: Filter rows with Units=0 and not Flat portfolios
        (Applied only to non-Bidding Adjustment rows)
        """
        # Filter Units = 0
        filtered = df[df["Units"] == 0].copy()

        # Exclude Flat portfolios
        portfolio_col = "Portfolio Name (Informational only)"
        if portfolio_col in filtered.columns:
            filtered = filtered[~filtered[portfolio_col].isin(self.FLAT_PORTFOLIOS)]

        # Keep only Keyword and Product Targeting
        filtered = filtered[
            filtered["Entity"].isin(["Keyword", "Product Targeting"])
        ].copy()

        return filtered

    def _add_helper_columns(
        self,
        main_df: pd.DataFrame,
        bidding_adj_df: pd.DataFrame,
        template_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Step 3: Add helper columns to main DataFrame
        IMPORTANT: Columns must be inserted to the LEFT of Bid column
        Order: ... | Max BA | Base Bid | Target CPA | Adj. CPA | Old Bid | Bid | ...
        """
        # Make a copy to avoid modifying original
        df_copy = main_df.copy()

        # Find the position of Bid column
        if "Bid" not in df_copy.columns:
            print("ERROR: Bid column not found!")
            return df_copy

        bid_column_index = df_copy.columns.get_loc("Bid")

        # FIRST - Store old bid values BEFORE any changes
        old_bid_values = df_copy["Bid"].values.copy()

        # Calculate Max BA for each Campaign ID
        max_ba_values = self._calculate_max_ba(df_copy, bidding_adj_df)

        # Get Base Bid and Target CPA from template
        base_bid_values = []
        target_cpa_values = []

        portfolio_col = "Portfolio Name (Informational only)"
        for _, row in df_copy.iterrows():
            portfolio = row.get(portfolio_col, "")
            base_bid = self.get_portfolio_value(
                portfolio, template_df, "Base Bid", default=0.02
            )
            target_cpa = self.get_portfolio_value(
                portfolio, template_df, "Target CPA", default=None
            )

            # Handle "Ignore" values
            if isinstance(base_bid, str) and base_bid.lower() == "ignore":
                base_bid = 0.02

            base_bid_values.append(base_bid)
            target_cpa_values.append(target_cpa)

        # Calculate derived columns
        adj_cpa_values = []
        for i in range(len(df_copy)):
            if pd.notna(target_cpa_values[i]):
                adj_cpa = target_cpa_values[i] * (1 + max_ba_values[i] / 100)
            else:
                adj_cpa = None
            adj_cpa_values.append(adj_cpa)

        # Calculate calc1 and calc2
        calc1_values = old_bid_values * 0.75  # 25% reduction
        calc2_values = base_bid_values

        # Insert helper columns to the LEFT of Bid column
        # Insert in reverse order so they appear in correct order
        # Final order should be: Max BA | Base Bid | Target CPA | Adj. CPA | calc1 | calc2 | Old Bid | Bid
        df_copy.insert(bid_column_index, "Old Bid", old_bid_values)
        df_copy.insert(bid_column_index, "calc2", calc2_values)
        df_copy.insert(bid_column_index, "calc1", calc1_values)
        df_copy.insert(bid_column_index, "Adj. CPA", adj_cpa_values)
        df_copy.insert(bid_column_index, "Target CPA", target_cpa_values)
        df_copy.insert(bid_column_index, "Base Bid", base_bid_values)
        df_copy.insert(bid_column_index, "Max BA", max_ba_values)

        return df_copy

    def _calculate_max_ba(
        self, main_df: pd.DataFrame, bidding_adj_df: pd.DataFrame
    ) -> List[float]:
        """
        Calculate Max BA for each row based on Campaign ID

        Returns list of Max BA values aligned with main_df rows
        """
        max_ba_values = []

        if len(bidding_adj_df) == 0:
            # No Bidding Adjustments, return 0 for all
            return [0.0] * len(main_df)

        # Get max percentage per campaign
        ba_max = bidding_adj_df.groupby("Campaign ID")["Percentage"].max().to_dict()

        # Map to main dataframe
        for _, row in main_df.iterrows():
            campaign_id = row.get("Campaign ID")
            max_ba = ba_max.get(campaign_id, 0)
            max_ba_values.append(max_ba)

        return max_ba_values

    def _calculate_bids(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Step 4: Calculate new bid values based on helper columns
        Formula: New Bid = MAX(calc1, calc2)
        """
        # Calculate new bid as max of calc1 and calc2
        df["Bid"] = df[["calc1", "calc2"]].max(axis=1)

        # Round to 2 decimal places
        df["Bid"] = df["Bid"].round(2)

        return df

    def check_bid_limits(self, df: pd.DataFrame) -> Tuple[int, int, int]:
        """
        Check if bids are within valid range [0.02, 1.25]

        Returns:
            Tuple of (below_count, above_count, error_count)
        """
        below_count = (df["Bid"] < 0.02).sum()
        above_count = (df["Bid"] > 1.25).sum()
        error_count = df["Bid"].isna().sum()

        # Highlight problematic rows
        if below_count > 0:
            df.loc[df["Bid"] < 0.02, "Bid_Status"] = "BELOW_MINIMUM"

        if above_count > 0:
            df.loc[df["Bid"] > 1.25, "Bid_Status"] = "ABOVE_MAXIMUM"

        if error_count > 0:
            df.loc[df["Bid"].isna(), "Bid_Status"] = "CALCULATION_ERROR"

        return below_count, above_count, error_count

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
            column: Column to get value from
            default: Default value if not found

        Returns:
            Value from template or default
        """
        if portfolio_name and column in template_df.columns:
            matches = template_df[template_df["Portfolio Name"] == portfolio_name]
            if not matches.empty:
                value = matches.iloc[0][column]
                # Convert to numeric if possible
                if pd.notna(value):
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        return value
        return default
