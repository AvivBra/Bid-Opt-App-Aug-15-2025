"""
bid-optimizer/business/processors/bulk_cleaner.py
Bulk Cleaner - Cleans and filters Bulk data according to business rules
"""

import pandas as pd
from typing import Dict, Any, List, Optional, Tuple


class BulkCleaner:
    """Cleans and filters Bulk file data"""

    # Valid entity types to keep
    VALID_ENTITIES = [
        "Keyword",
        "Product Targeting",
        "Product Ad",
        "Bidding Adjustment",
    ]

    # Required state value
    ENABLED_STATE = "enabled"

    def __init__(self):
        """Initialize cleaner"""
        self.cleaning_stats = {}
        self.removed_reasons = {}
        self.separated_dataframes = {}

    def clean_bulk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean Bulk DataFrame and separate into different entity types

        Filtering rules:
        1. Entity must be in VALID_ENTITIES
        2. Separate into 3 DataFrames: Targets, Product Ads, Bidding Adjustments
        3. Apply State filters only to Targets and Product Ads (NOT Bidding Adjustments)

        Args:
            df: Raw Bulk DataFrame

        Returns:
            Cleaned DataFrame (Targets only) for portfolio validation
        """
        # Track original count
        original_count = len(df)
        self.cleaning_stats = {"original_rows": original_count}
        self.removed_reasons = {}

        # Make a copy to avoid modifying original
        filtered_df = df.copy()

        # Step 1: Filter by Entity type
        if "Entity" in filtered_df.columns:
            before_count = len(filtered_df)
            filtered_df = filtered_df[filtered_df["Entity"].isin(self.VALID_ENTITIES)]
            removed = before_count - len(filtered_df)
            if removed > 0:
                self.removed_reasons["invalid_entity"] = removed
                self.cleaning_stats["after_entity_filter"] = len(filtered_df)

        # Step 2: Separate into 3 DataFrames
        targets_df = filtered_df[
            filtered_df["Entity"].isin(["Keyword", "Product Targeting"])
        ].copy()

        product_ads_df = filtered_df[filtered_df["Entity"] == "Product Ad"].copy()

        bidding_adjustments_df = filtered_df[
            filtered_df["Entity"] == "Bidding Adjustment"
        ].copy()

        # Track separation stats
        self.cleaning_stats["targets_before_state_filter"] = len(targets_df)
        self.cleaning_stats["product_ads_before_state_filter"] = len(product_ads_df)
        self.cleaning_stats["bidding_adjustments_count"] = len(bidding_adjustments_df)

        # Step 3: Apply State filters ONLY to Targets and Product Ads
        # NOT to Bidding Adjustments

        # Clean Targets
        if len(targets_df) > 0:
            targets_cleaned = self._apply_state_filters(targets_df, "Targets")
        else:
            targets_cleaned = targets_df

        # Clean Product Ads
        if len(product_ads_df) > 0:
            product_ads_cleaned = self._apply_state_filters(
                product_ads_df, "Product Ads"
            )
        else:
            product_ads_cleaned = product_ads_df

        # Bidding Adjustments - NO cleaning, pass through as-is
        bidding_adjustments_cleaned = bidding_adjustments_df

        # Store separated DataFrames
        self.separated_dataframes = {
            "targets": targets_cleaned,
            "product_ads": product_ads_cleaned,
            "bidding_adjustments": bidding_adjustments_cleaned,
        }

        # Update final stats
        self.cleaning_stats["targets_final"] = len(targets_cleaned)
        self.cleaning_stats["product_ads_final"] = len(product_ads_cleaned)
        self.cleaning_stats["bidding_adjustments_final"] = len(
            bidding_adjustments_cleaned
        )

        total_final = (
            len(targets_cleaned)
            + len(product_ads_cleaned)
            + len(bidding_adjustments_cleaned)
        )
        self.cleaning_stats["final_rows"] = total_final
        self.cleaning_stats["total_removed"] = original_count - total_final
        self.cleaning_stats["removal_percentage"] = (
            (original_count - total_final) / original_count * 100
            if original_count > 0
            else 0
        )

        # Return only Targets for portfolio validation
        # (as per spec: portfolio validation is done only on Targets)
        return targets_cleaned

    def _apply_state_filters(self, df: pd.DataFrame, entity_type: str) -> pd.DataFrame:
        """
        Apply State, Campaign State, and Ad Group State filters

        Args:
            df: DataFrame to filter
            entity_type: Type of entity for tracking

        Returns:
            Filtered DataFrame
        """
        original_count = len(df)
        filtered_df = df.copy()

        # Filter by State
        if "State" in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[filtered_df["State"] == self.ENABLED_STATE]
            removed = before - len(filtered_df)
            if removed > 0:
                self.removed_reasons[f"{entity_type}_state_not_enabled"] = removed

        # Filter by Campaign State
        campaign_state_col = "Campaign State (Informational only)"
        if campaign_state_col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[
                filtered_df[campaign_state_col] == self.ENABLED_STATE
            ]
            removed = before - len(filtered_df)
            if removed > 0:
                self.removed_reasons[f"{entity_type}_campaign_not_enabled"] = removed

        # Filter by Ad Group State
        ad_group_state_col = "Ad Group State (Informational only)"
        if ad_group_state_col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[
                filtered_df[ad_group_state_col] == self.ENABLED_STATE
            ]
            removed = before - len(filtered_df)
            if removed > 0:
                self.removed_reasons[f"{entity_type}_ad_group_not_enabled"] = removed

        # Reset index
        filtered_df = filtered_df.reset_index(drop=True)

        return filtered_df

    def get_separated_dataframes(self) -> Dict[str, pd.DataFrame]:
        """
        Get the separated DataFrames after cleaning

        Returns:
            Dictionary with 'targets', 'product_ads', 'bidding_adjustments' DataFrames
        """
        return self.separated_dataframes.copy()

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

        # Report on entity separation
        if self.cleaning_stats.get("targets_final", 0) > 0:
            messages.append(
                f"Targets (Keyword/Product Targeting): {self.cleaning_stats['targets_final']:,} rows"
            )

        if self.cleaning_stats.get("product_ads_final", 0) > 0:
            messages.append(
                f"Product Ads: {self.cleaning_stats['product_ads_final']:,} rows"
            )

        if self.cleaning_stats.get("bidding_adjustments_final", 0) > 0:
            messages.append(
                f"Bidding Adjustments: {self.cleaning_stats['bidding_adjustments_final']:,} rows (no state filtering applied)"
            )

        # Report on removals
        if self.cleaning_stats.get("total_removed", 0) > 0:
            messages.append(
                f"Total filtered out: {self.cleaning_stats['total_removed']:,} rows "
                f"({self.cleaning_stats.get('removal_percentage', 0):.1f}%)"
            )

            # Detail removal reasons
            for reason, count in self.removed_reasons.items():
                if "invalid_entity" in reason:
                    messages.append(f"  - {count:,} rows: Invalid Entity type")
                elif "state_not_enabled" in reason:
                    entity = reason.split("_")[0]
                    messages.append(f"  - {count:,} {entity} rows: State not enabled")
                elif "campaign_not_enabled" in reason:
                    entity = reason.split("_")[0]
                    messages.append(
                        f"  - {count:,} {entity} rows: Campaign not enabled"
                    )
                elif "ad_group_not_enabled" in reason:
                    entity = reason.split("_")[0]
                    messages.append(
                        f"  - {count:,} {entity} rows: Ad Group not enabled"
                    )

        else:
            messages.append("No rows were filtered out")

        summary["messages"] = messages

        return summary

    def validate_cleaning_result(self, cleaned_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate that cleaned data meets minimum requirements

        Args:
            cleaned_df: Cleaned DataFrame (Targets only)

        Returns:
            Validation result with issues and warnings
        """
        issues = []
        warnings = []

        # Check if Targets DataFrame is empty
        if len(cleaned_df) == 0:
            # Check if we have other entity types
            if self.cleaning_stats.get("product_ads_final", 0) > 0:
                warnings.append(
                    "No Keyword/Product Targeting rows found, but Product Ads exist"
                )
            elif self.cleaning_stats.get("bidding_adjustments_final", 0) > 0:
                warnings.append(
                    "No Keyword/Product Targeting rows found, but Bidding Adjustments exist"
                )
            else:
                issues.append("No valid rows remaining after cleaning")
        elif len(cleaned_df) < 10:
            warnings.append(
                f"Only {len(cleaned_df)} Keyword/Product Targeting rows remaining after filtering"
            )

        # Check portfolio coverage in Targets
        portfolio_column = "Portfolio Name (Informational only)"
        if portfolio_column in cleaned_df.columns:
            unique_portfolios = cleaned_df[portfolio_column].nunique()
            if unique_portfolios == 0:
                issues.append("No portfolios found in Targets data")
            elif unique_portfolios == 1:
                warnings.append("Only 1 portfolio found in Targets data")

        return {"is_valid": len(issues) == 0, "issues": issues, "warnings": warnings}

    def filter_bulk_by_ignored(
        self, bulk_df: pd.DataFrame, template_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove rows from Bulk that belong to ignored portfolios

        Args:
            bulk_df: Bulk DataFrame (already cleaned - Targets only)
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
