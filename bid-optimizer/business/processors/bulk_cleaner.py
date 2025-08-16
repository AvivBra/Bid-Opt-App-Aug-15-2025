"""
Bulk Cleaner
Cleans and filters Bulk data according to business rules
"""

import pandas as pd
from typing import Dict, Any, List, Optional


class BulkCleaner:
    """Cleans and filters Bulk file data"""

    # Valid entity types to keep
    VALID_ENTITIES = ["Keyword", "Product Targeting"]

    # Required state value
    ENABLED_STATE = "enabled"

    def __init__(self):
        """Initialize cleaner"""
        self.cleaning_stats = {}
        self.removed_reasons = {}

    def clean_bulk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean Bulk DataFrame by applying all filtering rules

        Filtering rules:
        1. Entity must be 'Keyword' or 'Product Targeting'
        2. State must be 'enabled'
        3. Campaign State must be 'enabled'
        4. Ad Group State must be 'enabled'

        Args:
            df: Raw Bulk DataFrame

        Returns:
            Cleaned DataFrame with only valid rows
        """
        # Track original count
        original_count = len(df)
        self.cleaning_stats = {"original_rows": original_count}
        self.removed_reasons = {}

        # Make a copy to avoid modifying original
        cleaned_df = df.copy()

        # Filter 1: Entity type
        if "Entity" in cleaned_df.columns:
            before_count = len(cleaned_df)
            cleaned_df = cleaned_df[cleaned_df["Entity"].isin(self.VALID_ENTITIES)]
            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["invalid_entity"] = removed
                self.cleaning_stats["after_entity_filter"] = len(cleaned_df)

        # Filter 2: State = enabled
        if "State" in cleaned_df.columns:
            before_count = len(cleaned_df)
            cleaned_df = cleaned_df[cleaned_df["State"] == self.ENABLED_STATE]
            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["state_not_enabled"] = removed
                self.cleaning_stats["after_state_filter"] = len(cleaned_df)

        # Filter 3: Campaign State = enabled
        campaign_state_col = "Campaign State (Informational only)"
        if campaign_state_col in cleaned_df.columns:
            before_count = len(cleaned_df)
            cleaned_df = cleaned_df[
                cleaned_df[campaign_state_col] == self.ENABLED_STATE
            ]
            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["campaign_not_enabled"] = removed
                self.cleaning_stats["after_campaign_filter"] = len(cleaned_df)

        # Filter 4: Ad Group State = enabled
        ad_group_state_col = "Ad Group State (Informational only)"
        if ad_group_state_col in cleaned_df.columns:
            before_count = len(cleaned_df)
            cleaned_df = cleaned_df[
                cleaned_df[ad_group_state_col] == self.ENABLED_STATE
            ]
            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["ad_group_not_enabled"] = removed
                self.cleaning_stats["after_ad_group_filter"] = len(cleaned_df)

        # Final stats
        self.cleaning_stats["final_rows"] = len(cleaned_df)
        self.cleaning_stats["total_removed"] = original_count - len(cleaned_df)
        self.cleaning_stats["removal_percentage"] = (
            (original_count - len(cleaned_df)) / original_count * 100
            if original_count > 0
            else 0
        )

        # Reset index for clean output
        cleaned_df = cleaned_df.reset_index(drop=True)

        return cleaned_df

    def get_cleaning_summary(self) -> Dict[str, Any]:
        """
        Get summary of cleaning operation

        Returns:
            Dictionary with cleaning statistics and reasons
        """
        summary = {
            "stats": self.cleaning_stats.copy(),
            "removal_reasons": self.removed_reasons.copy(),
        }

        # Add human-readable messages
        messages = []

        if self.cleaning_stats.get("total_removed", 0) > 0:
            messages.append(
                f"Filtered out {self.cleaning_stats['total_removed']:,} rows "
                f"({self.cleaning_stats.get('removal_percentage', 0):.1f}%)"
            )

            # Detail removal reasons
            for reason, count in self.removed_reasons.items():
                reason_text = {
                    "invalid_entity": f"Entity not Keyword/Product Targeting",
                    "state_not_enabled": f"State not enabled",
                    "campaign_not_enabled": f"Campaign not enabled",
                    "ad_group_not_enabled": f"Ad Group not enabled",
                }.get(reason, reason)
                messages.append(f"  • {count:,} rows: {reason_text}")
        else:
            messages.append("No rows filtered out - all rows are valid")

        summary["messages"] = messages

        return summary

    def extract_unique_portfolios(self, df: pd.DataFrame) -> List[str]:
        """
        Extract unique portfolio names from cleaned Bulk

        Args:
            df: Cleaned Bulk DataFrame

        Returns:
            List of unique portfolio names
        """
        portfolio_column = "Portfolio Name (Informational only)"

        if portfolio_column not in df.columns:
            return []

        # Get unique portfolios, handling NaN values
        portfolios = df[portfolio_column].dropna().astype(str).str.strip().unique()

        # Filter out empty strings
        portfolios = [p for p in portfolios if p]

        # Sort for consistent display
        portfolios.sort()

        return portfolios

    def get_portfolio_statistics(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Get statistics about portfolios in the Bulk

        Args:
            df: Cleaned Bulk DataFrame

        Returns:
            Dictionary with portfolio counts
        """
        portfolio_column = "Portfolio Name (Informational only)"

        if portfolio_column not in df.columns:
            return {}

        # Count rows per portfolio
        portfolio_counts = df[portfolio_column].value_counts().to_dict()

        return portfolio_counts

    def validate_cleaning_result(self, cleaned_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate that cleaning produced valid results

        Args:
            cleaned_df: Cleaned DataFrame

        Returns:
            Validation result
        """
        issues = []
        warnings = []

        # Check if empty
        if len(cleaned_df) == 0:
            issues.append("No valid rows after filtering - check your Bulk file")

        # Check if too few rows
        elif len(cleaned_df) < 10:
            warnings.append(f"Only {len(cleaned_df)} rows remaining after filtering")

        # Check portfolio coverage
        portfolio_column = "Portfolio Name (Informational only)"
        if portfolio_column in cleaned_df.columns:
            unique_portfolios = cleaned_df[portfolio_column].nunique()
            if unique_portfolios == 0:
                issues.append("No portfolios found in cleaned data")
            elif unique_portfolios == 1:
                warnings.append("Only 1 portfolio found in cleaned data")

        return {"is_valid": len(issues) == 0, "issues": issues, "warnings": warnings}

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
        # Get list of ignored portfolios (case-insensitive comparison)
        ignored = template_df[
            template_df["Base Bid"].astype(str).str.strip().str.lower() == "ignore"
        ]["Portfolio Name"].tolist()

        if not ignored:
            return bulk_df

        # Filter out ignored portfolios
        portfolio_column = "Portfolio Name (Informational only)"
        if portfolio_column in bulk_df.columns:
            filtered_df = bulk_df[~bulk_df[portfolio_column].isin(ignored)].copy()

            removed_count = len(bulk_df) - len(filtered_df)
            if removed_count > 0:
                self.removed_reasons["ignored_portfolios"] = removed_count
                messages = self.get_cleaning_summary().get("messages", [])
                messages.append(f"Removed {removed_count} rows from ignored portfolios")

            return filtered_df

        return bulk_df
