"""
Bulk Cleaner
Cleans and filters Bulk data according to business rules
"""

import pandas as pd
from typing import Dict, Any, List, Optional


class BulkCleaner:
    """Cleans and filters Bulk file data"""

    # Valid entity types to keep
    VALID_ENTITIES = ["Keyword", "Product Targeting", "Bidding Adjustment"]

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
        1. Entity must be 'Keyword' or 'Product Targeting' or 'Bidding Adjustment'
        2. State must be 'enabled' (EXCEPT for Bidding Adjustment)
        3. Campaign State must be 'enabled' (EXCEPT for Bidding Adjustment)
        4. Ad Group State must be 'enabled' (EXCEPT for Bidding Adjustment)

        Args:
            df: Raw Bulk DataFrame

        Returns:
            Cleaned DataFrame with only valid rows
        """
        # Track original count
        original_count = len(df)
        self.cleaning_stats = {"original_rows": original_count}
        self.removed_reasons = {}

        # DEBUG: Check for Bidding Adjustment BEFORE filtering
        if "Entity" in df.columns:
            entity_counts = df["Entity"].value_counts()
            print(f"DEBUG BulkCleaner: Entity counts BEFORE filtering:")
            for entity, count in entity_counts.items():
                print(f"  {entity}: {count}")

            bidding_adj_before = (df["Entity"] == "Bidding Adjustment").sum()
            print(
                f"DEBUG BulkCleaner: Bidding Adjustment rows BEFORE: {bidding_adj_before}"
            )

        # Make a copy to avoid modifying original
        cleaned_df = df.copy()

        # Filter 1: Entity type
        if "Entity" in cleaned_df.columns:
            before_count = len(cleaned_df)
            print(f"DEBUG BulkCleaner: VALID_ENTITIES = {self.VALID_ENTITIES}")
            cleaned_df = cleaned_df[cleaned_df["Entity"].isin(self.VALID_ENTITIES)]
            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["invalid_entity"] = removed
                self.cleaning_stats["after_entity_filter"] = len(cleaned_df)

            # DEBUG: Check after Entity filter
            bidding_adj_after_entity = (
                cleaned_df["Entity"] == "Bidding Adjustment"
            ).sum()
            print(
                f"DEBUG BulkCleaner: Bidding Adjustment rows AFTER Entity filter: {bidding_adj_after_entity}"
            )

        # Filter 2: State = enabled (EXCEPT for Bidding Adjustment)
        if "State" in cleaned_df.columns:
            before_count = len(cleaned_df)

            # DEBUG: Check State values for Bidding Adjustment
            bidding_adj_mask = cleaned_df["Entity"] == "Bidding Adjustment"
            if bidding_adj_mask.any():
                ba_states = cleaned_df[bidding_adj_mask]["State"].value_counts()
                print(f"DEBUG BulkCleaner: Bidding Adjustment State values:")
                for state, count in ba_states.items():
                    print(f"  {state}: {count}")

            # IMPORTANT: Apply State filter ONLY to non-Bidding Adjustment rows
            # Bidding Adjustment rows ALWAYS pass through regardless of State value
            state_filter = (cleaned_df["State"] == self.ENABLED_STATE) | (
                cleaned_df["Entity"] == "Bidding Adjustment"
            )
            cleaned_df = cleaned_df[state_filter]

            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["state_not_enabled"] = removed
                self.cleaning_stats["after_state_filter"] = len(cleaned_df)

            # DEBUG: Check after State filter
            bidding_adj_after_state = (
                cleaned_df["Entity"] == "Bidding Adjustment"
            ).sum()
            print(
                f"DEBUG BulkCleaner: Bidding Adjustment rows AFTER State filter: {bidding_adj_after_state}"
            )

        # Filter 3: Campaign State = enabled (EXCEPT for Bidding Adjustment)
        campaign_state_col = "Campaign State (Informational only)"
        if campaign_state_col in cleaned_df.columns:
            before_count = len(cleaned_df)

            # DEBUG: Check Campaign State for Bidding Adjustment
            bidding_adj_mask = cleaned_df["Entity"] == "Bidding Adjustment"
            if bidding_adj_mask.any():
                ba_campaign_states = cleaned_df[bidding_adj_mask][
                    campaign_state_col
                ].value_counts()
                print(f"DEBUG BulkCleaner: Bidding Adjustment Campaign State values:")
                for state, count in ba_campaign_states.items():
                    print(f"  {state}: {count}")

            # IMPORTANT: Apply Campaign State filter ONLY to non-Bidding Adjustment rows
            # Bidding Adjustment rows ALWAYS pass through regardless of Campaign State
            campaign_filter = (cleaned_df[campaign_state_col] == self.ENABLED_STATE) | (
                cleaned_df["Entity"] == "Bidding Adjustment"
            )
            cleaned_df = cleaned_df[campaign_filter]

            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["campaign_not_enabled"] = removed
                self.cleaning_stats["after_campaign_filter"] = len(cleaned_df)

            # DEBUG: Check after Campaign State filter
            bidding_adj_after_campaign = (
                cleaned_df["Entity"] == "Bidding Adjustment"
            ).sum()
            print(
                f"DEBUG BulkCleaner: Bidding Adjustment rows AFTER Campaign State filter: {bidding_adj_after_campaign}"
            )

        # Filter 4: Ad Group State = enabled (EXCEPT for Bidding Adjustment)
        ad_group_state_col = "Ad Group State (Informational only)"
        if ad_group_state_col in cleaned_df.columns:
            before_count = len(cleaned_df)

            # DEBUG: Check Ad Group State for Bidding Adjustment
            bidding_adj_mask = cleaned_df["Entity"] == "Bidding Adjustment"
            if bidding_adj_mask.any():
                ba_adgroup_states = cleaned_df[bidding_adj_mask][
                    ad_group_state_col
                ].value_counts()
                print(f"DEBUG BulkCleaner: Bidding Adjustment Ad Group State values:")
                for state, count in ba_adgroup_states.items():
                    print(f"  {state}: {count}")

            # IMPORTANT: Apply Ad Group State filter ONLY to non-Bidding Adjustment rows
            # Bidding Adjustment rows ALWAYS pass through regardless of Ad Group State
            ad_group_filter = (cleaned_df[ad_group_state_col] == self.ENABLED_STATE) | (
                cleaned_df["Entity"] == "Bidding Adjustment"
            )
            cleaned_df = cleaned_df[ad_group_filter]

            removed = before_count - len(cleaned_df)
            if removed > 0:
                self.removed_reasons["ad_group_not_enabled"] = removed
                self.cleaning_stats["after_ad_group_filter"] = len(cleaned_df)

            # DEBUG: Check after Ad Group State filter
            bidding_adj_final = (cleaned_df["Entity"] == "Bidding Adjustment").sum()
            print(
                f"DEBUG BulkCleaner: Bidding Adjustment rows FINAL: {bidding_adj_final}"
            )

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

        # DEBUG: Final check
        print(
            f"DEBUG BulkCleaner: Final unique Entity values: {cleaned_df['Entity'].unique() if 'Entity' in cleaned_df.columns else 'No Entity column'}"
        )

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
                    "invalid_entity": f"Entity not Keyword/Product Targeting/Bidding Adjustment",
                    "state_not_enabled": f"State not enabled",
                    "campaign_not_enabled": f"Campaign not enabled",
                    "ad_group_not_enabled": f"Ad Group not enabled",
                }.get(reason, reason)

                messages.append(f"  - {count:,} rows: {reason_text}")

        else:
            messages.append("No rows were filtered out")

        summary["messages"] = messages

        return summary

    def validate_cleaning_result(self, cleaned_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate that cleaned data meets minimum requirements

        Args:
            cleaned_df: Cleaned DataFrame

        Returns:
            Validation result with issues and warnings
        """
        issues = []
        warnings = []

        # Check if empty
        if len(cleaned_df) == 0:
            issues.append("No valid rows remaining after cleaning")

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
