"""
Mock Bulk Data
נתוני דמה לקובץ Bulk עם 48 עמודות
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from io import BytesIO
from datetime import datetime, timedelta


class MockBulkData:
    """Mock bulk data generator for testing"""

    # Column names for Amazon Bulk file
    BULK_COLUMNS = [
        "Product",
        "Entity",
        "Operation",
        "Campaign ID",
        "Ad Group ID",
        "Portfolio ID",
        "Ad ID",
        "Keyword ID",
        "Product Targeting ID",
        "Campaign Name",
        "Ad Group Name",
        "Campaign Name (Informational only)",
        "Ad Group Name (Informational only)",
        "Portfolio Name (Informational only)",
        "Start Date",
        "End Date",
        "Targeting Type",
        "State",
        "Campaign State (Informational only)",
        "Ad Group State (Informational only)",
        "Daily Budget",
        "SKU",
        "ASIN",
        "Eligibility Status (Informational only)",
        "Reason for Ineligibility (Informational only)",
        "Ad Group Default Bid",
        "Ad Group Default Bid (Informational only)",
        "Bid",
        "Keyword Text",
        "Native Language Keyword",
        "Native Language Locale",
        "Match Type",
        "Bidding Strategy",
        "Placement",
        "Percentage",
        "Product Targeting Expression",
        "Resolved Product Targeting Expression (Informational only)",
        "Impressions",
        "Clicks",
        "Click-through Rate",
        "Spend",
        "Sales",
        "Orders",
        "Units",
        "Conversion Rate",
        "ACOS",
        "CPC",
        "ROAS",
    ]

    @staticmethod
    def generate_bulk_data(
        num_rows: int = 100, portfolios: List[str] = None
    ) -> pd.DataFrame:
        """
        Generate mock bulk data

        Args:
            num_rows: Number of rows to generate
            portfolios: List of portfolio names to use

        Returns:
            DataFrame with 48 columns
        """
        if portfolios is None:
            portfolios = [
                "Kids-Brand-US",
                "Kids-Brand-EU",
                "Supplements-US",
                "Supplements-EU",
            ]

        # Set random seed for consistency
        np.random.seed(42)

        data = {}

        # Basic columns
        data["Product"] = ["ASIN" + str(i % 20).zfill(3) for i in range(num_rows)]

        # Entity distribution: 50% Keyword, 40% Product Targeting, 10% Other
        entity_choices = (
            ["Keyword"] * 50
            + ["Product Targeting"] * 40
            + ["Campaign"] * 5
            + ["Ad Group"] * 5
        )
        data["Entity"] = np.random.choice(entity_choices, num_rows)

        data["Operation"] = ["Create"] * (num_rows // 2) + ["Update"] * (num_rows // 2)

        # IDs
        data["Campaign ID"] = ["123456789" + str(i % 10) for i in range(num_rows)]
        data["Ad Group ID"] = ["987654321" + str(i % 10) for i in range(num_rows)]
        data["Portfolio ID"] = ["111111111" + str(i % 4) for i in range(num_rows)]
        data["Ad ID"] = [""] * num_rows
        data["Keyword ID"] = [""] * num_rows
        data["Product Targeting ID"] = [""] * num_rows

        # Names
        data["Campaign Name"] = ["Campaign-" + str(i % 5) for i in range(num_rows)]
        data["Ad Group Name"] = ["AdGroup-" + str(i % 10) for i in range(num_rows)]
        data["Campaign Name (Informational only)"] = data["Campaign Name"]
        data["Ad Group Name (Informational only)"] = data["Ad Group Name"]

        # Portfolio distribution
        data["Portfolio Name (Informational only)"] = [
            portfolios[i % len(portfolios)] for i in range(num_rows)
        ]

        # Dates
        data["Start Date"] = ["01/01/2024"] * num_rows
        data["End Date"] = [""] * num_rows

        # Settings
        data["Targeting Type"] = ["MANUAL"] * (num_rows * 7 // 10) + ["AUTO"] * (
            num_rows * 3 // 10
        )

        # States - important for filtering
        # 80% enabled, 15% paused, 5% archived
        state_choices = ["enabled"] * 80 + ["paused"] * 15 + ["archived"] * 5
        data["State"] = np.random.choice(state_choices, num_rows)

        # Campaign and Ad Group states (90% enabled)
        campaign_state_choices = ["enabled"] * 90 + ["paused"] * 10
        data["Campaign State (Informational only)"] = np.random.choice(
            campaign_state_choices, num_rows
        )
        data["Ad Group State (Informational only)"] = np.random.choice(
            campaign_state_choices, num_rows
        )

        # Budget and Bids
        data["Daily Budget"] = np.round(np.random.uniform(5, 100, num_rows), 2)
        data["SKU"] = ["SKU" + str(i).zfill(5) for i in range(num_rows)]
        data["ASIN"] = ["B00" + str(i).zfill(7) for i in range(num_rows)]

        # Status
        data["Eligibility Status (Informational only)"] = [""] * num_rows
        data["Reason for Ineligibility (Informational only)"] = [""] * num_rows

        # Bids
        data["Ad Group Default Bid"] = np.round(
            np.random.uniform(0.5, 3.0, num_rows), 3
        )
        data["Ad Group Default Bid (Informational only)"] = data["Ad Group Default Bid"]
        data["Bid"] = np.round(np.random.uniform(0.5, 3.0, num_rows), 3)

        # Keywords
        data["Keyword Text"] = ["keyword " + str(i) for i in range(num_rows)]
        data["Native Language Keyword"] = [""] * num_rows
        data["Native Language Locale"] = [""] * num_rows

        # Match Type
        match_choices = ["BROAD"] * 50 + ["PHRASE"] * 30 + ["EXACT"] * 20
        data["Match Type"] = np.random.choice(match_choices, num_rows)

        # Strategy
        data["Bidding Strategy"] = [""] * num_rows
        data["Placement"] = [""] * num_rows
        data["Percentage"] = [""] * num_rows

        # Targeting
        data["Product Targeting Expression"] = [""] * num_rows
        data["Resolved Product Targeting Expression (Informational only)"] = [
            ""
        ] * num_rows

        # Performance metrics
        data["Impressions"] = np.random.randint(0, 10000, num_rows)
        data["Clicks"] = np.random.randint(0, 500, num_rows)
        data["Click-through Rate"] = np.round(
            data["Clicks"] / np.maximum(data["Impressions"], 1), 4
        )
        data["Spend"] = np.round(np.random.uniform(0, 500, num_rows), 2)

        # Sales - 30% with zero sales (important for Zero Sales optimization)
        sales_values = np.random.uniform(0, 1000, num_rows)
        sales_values[np.random.choice(num_rows, num_rows * 3 // 10, replace=False)] = 0
        data["Sales"] = np.round(sales_values, 2)

        data["Orders"] = np.where(
            data["Sales"] > 0, np.random.randint(1, 20, num_rows), 0
        )
        data["Units"] = np.where(
            data["Sales"] > 0, np.random.randint(1, 50, num_rows), 0
        )

        # Conversion metrics
        data["Conversion Rate"] = np.round(
            np.where(data["Clicks"] > 0, data["Orders"] / data["Clicks"], 0), 4
        )
        data["ACOS"] = np.round(
            np.where(data["Sales"] > 0, (data["Spend"] / data["Sales"]) * 100, 0), 2
        )
        data["CPC"] = np.round(
            np.where(data["Clicks"] > 0, data["Spend"] / data["Clicks"], 0), 3
        )
        data["ROAS"] = np.round(
            np.where(data["Spend"] > 0, data["Sales"] / data["Spend"], 0), 2
        )

        return pd.DataFrame(data)

    @staticmethod
    def get_small_bulk() -> pd.DataFrame:
        """Get small bulk file (100 rows) for quick testing"""
        return MockBulkData.generate_bulk_data(100)

    @staticmethod
    def get_medium_bulk() -> pd.DataFrame:
        """Get medium bulk file (10K rows) for performance testing"""
        return MockBulkData.generate_bulk_data(10000)

    @staticmethod
    def get_large_bulk() -> pd.DataFrame:
        """Get large bulk file (100K rows) for stress testing"""
        return MockBulkData.generate_bulk_data(100000)

    @staticmethod
    def get_max_bulk() -> pd.DataFrame:
        """Get maximum size bulk file (499K rows) just under limit"""
        return MockBulkData.generate_bulk_data(499000)

    @staticmethod
    def get_over_limit_bulk() -> pd.DataFrame:
        """Get over-limit bulk file (501K rows) for error testing"""
        return MockBulkData.generate_bulk_data(501000)

    @staticmethod
    def get_cleaned_bulk(df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Get cleaned bulk data (after filtering)
        Simulates the bulk cleaning process
        """
        if df is None:
            df = MockBulkData.get_small_bulk()

        # Apply cleaning filters
        cleaned = df[
            (df["Entity"].isin(["Keyword", "Product Targeting"]))
            & (df["State"] == "enabled")
            & (df["Campaign State (Informational only)"] == "enabled")
            & (df["Ad Group State (Informational only)"] == "enabled")
        ].copy()

        return cleaned

    @staticmethod
    def create_bulk_file(num_rows: int = 100, portfolios: List[str] = None) -> BytesIO:
        """
        Create Excel file with bulk data

        Args:
            num_rows: Number of rows
            portfolios: Portfolio names to use

        Returns:
            BytesIO object containing Excel file
        """
        df = MockBulkData.generate_bulk_data(num_rows, portfolios)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Sponsored Products Campaigns", index=False)

        output.seek(0)
        return output

    @staticmethod
    def create_invalid_bulk_file(error_type: str = "missing_sheet") -> BytesIO:
        """
        Create invalid bulk file for error testing

        Args:
            error_type: Type of error ('missing_sheet', 'wrong_columns', 'empty')
        """
        output = BytesIO()

        if error_type == "missing_sheet":
            # Wrong sheet name
            df = MockBulkData.get_small_bulk()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Wrong Sheet Name", index=False)

        elif error_type == "wrong_columns":
            # Missing required columns
            df = pd.DataFrame({"Column1": [1, 2, 3], "Column2": ["a", "b", "c"]})
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(
                    writer, sheet_name="Sponsored Products Campaigns", index=False
                )

        elif error_type == "empty":
            # Empty file
            df = pd.DataFrame(columns=MockBulkData.BULK_COLUMNS)
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(
                    writer, sheet_name="Sponsored Products Campaigns", index=False
                )

        output.seek(0)
        return output

    @staticmethod
    def get_bulk_stats(df: pd.DataFrame) -> Dict:
        """
        Get statistics about bulk data

        Returns:
            Dictionary with bulk statistics
        """
        cleaned = MockBulkData.get_cleaned_bulk(df)

        return {
            "total_rows": len(df),
            "cleaned_rows": len(cleaned),
            "filtered_out": len(df) - len(cleaned),
            "unique_portfolios": df["Portfolio Name (Informational only)"].nunique(),
            "entities": df["Entity"].value_counts().to_dict(),
            "states": df["State"].value_counts().to_dict(),
            "zero_sales_count": len(df[df["Sales"] == 0]),
            "file_size_mb": round(len(df) * 0.023, 1),  # Approximate size
        }
