"""
Mock Data Provider
Provides mock data for testing different scenarios
"""

import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List, Tuple


class MockDataProvider:
    """Provides mock data for different scenarios"""

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
    def get_mock_template_valid() -> pd.DataFrame:
        """Get valid template with all portfolios"""
        return pd.DataFrame(
            {
                "Portfolio Name": [
                    "Kids-Brand-US",
                    "Kids-Brand-EU",
                    "Supplements-US",
                    "Supplements-EU",
                ],
                "Base Bid": [1.25, 0.95, 2.10, 1.85],
                "Target CPA": [5.00, 4.50, 8.00, 7.50],
            }
        )

    @staticmethod
    def get_mock_template_missing() -> pd.DataFrame:
        """Get template with missing portfolios"""
        return pd.DataFrame(
            {
                "Portfolio Name": ["Kids-Brand-US", "Kids-Brand-EU"],
                "Base Bid": [1.25, 0.95],
                "Target CPA": [5.00, 4.50],
            }
        )

    @staticmethod
    def get_mock_template_excess() -> pd.DataFrame:
        """Get template with excess portfolios"""
        return pd.DataFrame(
            {
                "Portfolio Name": [
                    "Kids-Brand-US",
                    "Kids-Brand-EU",
                    "Supplements-US",
                    "Supplements-EU",
                    "Electronics-US",  # Extra
                    "Electronics-EU",  # Extra
                ],
                "Base Bid": [1.25, 0.95, 2.10, 1.85, 1.50, 1.75],
                "Target CPA": [5.00, 4.50, 8.00, 7.50, 6.00, 6.50],
            }
        )

    @staticmethod
    def get_mock_template_mixed() -> pd.DataFrame:
        """Get template with mixed issues"""
        return pd.DataFrame(
            {
                "Portfolio Name": [
                    "Kids-Brand-US",
                    "Kids-Brand-EU",
                    "Supplements-US",  # Will be set to Ignore
                    "Electronics-US",  # Extra (not in bulk)
                    "NewProduct-US",  # Extra (not in bulk)
                ],
                "Base Bid": [1.25, 0.95, "Ignore", 1.50, 2.00],
                "Target CPA": [5.00, 4.50, None, 6.00, 10.00],
            }
        )

    @staticmethod
    def get_mock_template_ignored() -> pd.DataFrame:
        """Get template with ignored portfolios"""
        return pd.DataFrame(
            {
                "Portfolio Name": [
                    "Kids-Brand-US",
                    "Kids-Brand-EU",
                    "Supplements-US",
                    "Supplements-EU",
                    "Electronics-US",
                    "Electronics-EU",
                ],
                "Base Bid": [1.25, 0.95, "Ignore", "Ignore", 1.50, "Ignore"],
                "Target CPA": [5.00, 4.50, None, None, 6.00, None],
            }
        )

    @staticmethod
    def get_mock_bulk_data(
        num_rows: int = 100, portfolios: List[str] = None
    ) -> pd.DataFrame:
        """
        Get mock bulk data with 46 columns

        Args:
            num_rows: Number of rows to generate
            portfolios: List of portfolio names to use
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
    def get_cleaned_bulk(df: pd.DataFrame = None) -> pd.DataFrame:
        """Get cleaned bulk data (after filtering)"""
        if df is None:
            df = MockDataProvider.get_mock_bulk_data()

        # Apply cleaning filters
        cleaned = df[
            (df["Entity"].isin(["Keyword", "Product Targeting"]))
            & (df["State"] == "enabled")
            & (df["Campaign State (Informational only)"] == "enabled")
            & (df["Ad Group State (Informational only)"] == "enabled")
        ].copy()

        return cleaned

    @staticmethod
    def create_mock_excel_file(file_type: str = "template") -> BytesIO:
        """Create mock Excel file"""
        output = BytesIO()

        if file_type == "template":
            df = MockDataProvider.get_mock_template_valid()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Template", index=False)

        elif file_type == "bulk":
            df = MockDataProvider.get_mock_bulk_data()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(
                    writer, sheet_name="Sponsored Products Campaigns", index=False
                )

        elif file_type == "working":
            # Working file has 2 sheets per optimization
            df = MockDataProvider.get_cleaned_bulk()
            df["Operation"] = "Update"
            df["Bid"] = 0.02  # Simulated Zero Sales optimization

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                # Clean sheet - just the updated bulk data
                df.to_excel(writer, sheet_name="Clean Zero Sales", index=False)
                # Working sheet - same data (in real app would have extra columns)
                df.to_excel(writer, sheet_name="Working Zero Sales", index=False)

        elif file_type == "clean":
            # Clean file has 1 sheet per optimization
            df = MockDataProvider.get_cleaned_bulk()
            df["Operation"] = "Update"
            df["Bid"] = 0.02  # Simulated Zero Sales optimization

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Clean Zero Sales", index=False)

        output.seek(0)
        return output

    @staticmethod
    def get_validation_scenarios() -> Dict[str, Dict[str, Any]]:
        """Get all validation scenarios"""
        return {
            "valid": {
                "is_valid": True,
                "missing_portfolios": [],
                "ignored_portfolios": [],
                "excess_portfolios": [],
                "messages": ["✓ All portfolios valid"],
                "stats": {
                    "total_portfolios": 6,
                    "valid_rows": 1234,
                    "filtered_rows": 856,
                },
            },
            "missing": {
                "is_valid": False,
                "missing_portfolios": [
                    "Supplements-EU",
                    "Electronics-US",
                    "Electronics-EU",
                ],
                "ignored_portfolios": [],
                "excess_portfolios": [],
                "messages": ["Missing portfolios found"],
                "stats": {
                    "total_portfolios": 6,
                    "valid_rows": 500,
                    "filtered_rows": 320,
                },
            },
            "ignored": {
                "is_valid": True,
                "missing_portfolios": [],
                "ignored_portfolios": [
                    "Supplements-US",
                    "Supplements-EU",
                    "Electronics-EU",
                ],
                "excess_portfolios": [],
                "messages": ["Some portfolios marked as Ignore"],
                "stats": {
                    "total_portfolios": 6,
                    "valid_rows": 800,
                    "filtered_rows": 550,
                },
            },
            "mixed": {
                "is_valid": False,
                "missing_portfolios": ["NewProduct-US"],
                "ignored_portfolios": ["Electronics-EU"],
                "excess_portfolios": [],
                "messages": ["Missing portfolios and some ignored"],
                "stats": {
                    "total_portfolios": 7,
                    "valid_rows": 900,
                    "filtered_rows": 600,
                },
            },
        }

    @staticmethod
    def get_mock_scenarios() -> Dict[str, Dict[str, Any]]:
        """Get all predefined test scenarios"""

        # Valid scenario
        valid_template = MockDataProvider.get_mock_template_valid()
        valid_bulk = MockDataProvider.get_mock_bulk_data(100)
        valid_cleaned = MockDataProvider.get_cleaned_bulk(valid_bulk)

        # Missing scenario
        missing_template = MockDataProvider.get_mock_template_missing()
        missing_bulk = MockDataProvider.get_mock_bulk_data(100)
        missing_cleaned = MockDataProvider.get_cleaned_bulk(missing_bulk)
        missing_portfolios = list(
            set(missing_cleaned["Portfolio Name (Informational only)"].unique())
            - set(missing_template["Portfolio Name"].tolist())
        )

        return {
            "valid": {
                "name": "✅ Valid - All Portfolios Match",
                "template_df": valid_template,
                "bulk_df": valid_bulk,
                "cleaned_df": valid_cleaned,
                "validation_result": {
                    "is_valid": True,
                    "missing_portfolios": [],
                    "excess_portfolios": [],
                    "ignored_portfolios": [],
                    "messages": ["✓ All portfolios valid"],
                    "errors": [],
                },
                "stats": {
                    "template_portfolios": 4,
                    "bulk_portfolios": 4,
                    "original_rows": 100,
                    "cleaned_rows": len(valid_cleaned),
                },
            },
            "missing": {
                "name": "❌ Missing - Portfolios Missing (Blocked)",
                "template_df": missing_template,
                "bulk_df": missing_bulk,
                "cleaned_df": missing_cleaned,
                "validation_result": {
                    "is_valid": False,
                    "missing_portfolios": missing_portfolios,
                    "excess_portfolios": [],
                    "ignored_portfolios": [],
                    "messages": ["❌ Missing portfolios found - Processing Blocked"],
                    "errors": [f"Missing portfolios: {', '.join(missing_portfolios)}"],
                },
                "stats": {
                    "template_portfolios": 2,
                    "bulk_portfolios": 4,
                    "original_rows": 100,
                    "cleaned_rows": len(missing_cleaned),
                },
            },
        }

    @staticmethod
    def create_scenario_files(scenario_name: str) -> Tuple[BytesIO, BytesIO]:
        """Create Excel files for a specific scenario"""
        scenarios = MockDataProvider.get_mock_scenarios()
        scenario = scenarios.get(scenario_name, scenarios["valid"])

        # Create template file
        template_output = BytesIO()
        with pd.ExcelWriter(template_output, engine="openpyxl") as writer:
            scenario["template_df"].to_excel(writer, sheet_name="Template", index=False)
        template_output.seek(0)

        # Create bulk file
        bulk_output = BytesIO()
        with pd.ExcelWriter(bulk_output, engine="openpyxl") as writer:
            scenario["bulk_df"].to_excel(
                writer, sheet_name="Sponsored Products Campaigns", index=False
            )
        bulk_output.seek(0)

        return template_output, bulk_output

    @staticmethod
    def get_processing_stats() -> Dict[str, Any]:
        """Get mock processing statistics"""
        return {
            "rows_processed": 1234,
            "rows_modified": 456,
            "calculation_errors": 7,
            "high_bids": 3,
            "low_bids": 2,
            "processing_time": 2.3,
            "optimizations_applied": ["Zero Sales"],
        }

    @staticmethod
    def get_file_stats() -> Dict[str, Dict[str, Any]]:
        """Get mock file statistics"""
        return {
            "working_file": {"size_mb": 2.4, "sheets": 2, "rows": 1234},
            "clean_file": {"size_mb": 1.8, "sheets": 1, "rows": 1234},
        }

    @staticmethod
    def generate_output_filename(file_type: str) -> str:
        """Generate output filename with timestamp"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M")
        return f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"


class MockFile:
    """Mock file object for testing"""

    def __init__(self, name: str, size: int, content: bytes = None):
        self.name = name
        self.size = size
        self._content = content or b"Mock file content"

    def read(self) -> bytes:
        return self._content

    def getvalue(self) -> bytes:
        return self._content

    def __len__(self) -> int:
        return self.size
