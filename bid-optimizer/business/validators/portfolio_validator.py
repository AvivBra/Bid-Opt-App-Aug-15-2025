"""
Portfolio Validator
Validates portfolio matching between Template and Bulk files
"""

import pandas as pd
from typing import Dict, List, Any, Set


class PortfolioValidator:
    """Validates portfolio consistency between Template and Bulk files"""

    def __init__(self):
        """Initialize validator"""
        self.missing_portfolios = []
        self.excess_portfolios = []
        self.ignored_portfolios = []
        self.validation_messages = []

    def validate_portfolios(
        self, template_df: pd.DataFrame, cleaned_bulk_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Validate that all portfolios in cleaned Bulk exist in Template

        Args:
            template_df: Template DataFrame with portfolio definitions
            cleaned_bulk_df: Cleaned Bulk DataFrame (after filtering)

        Returns:
            Validation result with missing/excess/ignored portfolios
        """
        # Reset state
        self.missing_portfolios = []
        self.excess_portfolios = []
        self.ignored_portfolios = []
        self.validation_messages = []

        # Get portfolios from Template (excluding ignored)
        template_portfolios = set()
        template_all = set()

        for _, row in template_df.iterrows():
            portfolio_name = str(row["Portfolio Name"]).strip()
            base_bid = str(row["Base Bid"]).strip()

            template_all.add(portfolio_name)

            if base_bid.lower() == "ignore":
                self.ignored_portfolios.append(portfolio_name)
            else:
                template_portfolios.add(portfolio_name)

        # Get unique portfolios from cleaned Bulk
        bulk_portfolios = set()

        portfolio_column = "Portfolio Name (Informational only)"
        if portfolio_column in cleaned_bulk_df.columns:
            bulk_portfolios = set(
                cleaned_bulk_df[portfolio_column]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
            )

        # Find missing portfolios (in Bulk but not in Template)
        self.missing_portfolios = list(bulk_portfolios - template_portfolios)

        # Remove ignored portfolios from missing list
        ignored_set = set(self.ignored_portfolios)
        self.missing_portfolios = [
            p for p in self.missing_portfolios if p not in ignored_set
        ]

        # Find excess portfolios (in Template but not in Bulk)
        self.excess_portfolios = list(template_portfolios - bulk_portfolios)

        # Create validation result
        is_valid = len(self.missing_portfolios) == 0

        # Generate messages
        if is_valid:
            if self.ignored_portfolios:
                self.validation_messages.append("✓ All portfolios valid (some ignored)")
            else:
                self.validation_messages.append("✓ All portfolios valid")
                self.validation_messages.append(
                    "All portfolios in Bulk file have Base Bid values in Template"
                )
        else:
            # Add count to the error message
            missing_count = len(self.missing_portfolios)
            self.validation_messages.append(
                f"❌ Missing portfolios found ({missing_count})"
            )

            if self.missing_portfolios:
                # Show first 5 portfolios with count
                if missing_count <= 5:
                    self.validation_messages.append(
                        f"The following {missing_count} portfolios are in Bulk but not in Template: {', '.join(self.missing_portfolios)}"
                    )
                else:
                    self.validation_messages.append(
                        f"The following {missing_count} portfolios are in Bulk but not in Template: {', '.join(self.missing_portfolios[:5])}"
                    )
                    self.validation_messages.append(f"... and {missing_count - 5} more")

        # Add warnings for ignored portfolios with count
        if self.ignored_portfolios:
            ignored_count = len(self.ignored_portfolios)
            self.validation_messages.append(f"ℹ️ Ignored portfolios: {ignored_count}")

        # Add info about excess portfolios (not blocking) with count
        if self.excess_portfolios:
            excess_count = len(self.excess_portfolios)
            self.validation_messages.append(
                f"ℹ️ {excess_count} portfolios in Template not found in Bulk (not blocking)"
            )

        return self._create_result(is_valid)

    def get_portfolio_summary(
        self, template_df: pd.DataFrame, cleaned_bulk_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Get detailed portfolio summary statistics

        Args:
            template_df: Template DataFrame
            cleaned_bulk_df: Cleaned Bulk DataFrame

        Returns:
            Summary statistics dictionary
        """
        portfolio_column = "Portfolio Name (Informational only)"

        # Count portfolios
        template_count = len(template_df)
        template_valid = len(template_df[template_df["Base Bid"] != "Ignore"])
        template_ignored = len(template_df[template_df["Base Bid"] == "Ignore"])

        bulk_unique = 0
        if portfolio_column in cleaned_bulk_df.columns:
            bulk_unique = cleaned_bulk_df[portfolio_column].nunique()

        # Count rows per portfolio in Bulk
        portfolio_row_counts = {}
        if portfolio_column in cleaned_bulk_df.columns:
            portfolio_row_counts = (
                cleaned_bulk_df[portfolio_column].value_counts().to_dict()
            )

        return {
            "template_total": template_count,
            "template_valid": template_valid,
            "template_ignored": template_ignored,
            "bulk_unique_portfolios": bulk_unique,
            "bulk_total_rows": len(cleaned_bulk_df),
            "portfolio_row_counts": portfolio_row_counts,
            "missing_count": len(self.missing_portfolios),
            "excess_count": len(self.excess_portfolios),
            "ignored_count": len(self.ignored_portfolios),
        }

    def filter_bulk_by_ignored(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove rows from Bulk that belong to ignored portfolios

        Args:
            bulk_df: Bulk DataFrame (already cleaned)
            template_df: Template DataFrame

        Returns:
            Filtered DataFrame without ignored portfolio rows
        """
        # Get list of ignored portfolios
        ignored = template_df[template_df["Base Bid"] == "Ignore"][
            "Portfolio Name"
        ].tolist()

        if not ignored:
            return bulk_df

        # Filter out ignored portfolios
        portfolio_column = "Portfolio Name (Informational only)"
        if portfolio_column in bulk_df.columns:
            filtered_df = bulk_df[~bulk_df[portfolio_column].isin(ignored)].copy()

            removed_count = len(bulk_df) - len(filtered_df)
            if removed_count > 0:
                self.validation_messages.append(
                    f"Removed {removed_count} rows from ignored portfolios"
                )

            return filtered_df

        return bulk_df

    def _create_result(self, is_valid: bool) -> Dict[str, Any]:
        """Create validation result dictionary"""
        return {
            "is_valid": is_valid,
            "missing_portfolios": self.missing_portfolios.copy(),
            "excess_portfolios": self.excess_portfolios.copy(),
            "ignored_portfolios": self.ignored_portfolios.copy(),
            "messages": self.validation_messages.copy(),
            "portfolio_counts": {
                "missing": len(self.missing_portfolios),
                "excess": len(self.excess_portfolios),
                "ignored": len(self.ignored_portfolios),
            },
        }
