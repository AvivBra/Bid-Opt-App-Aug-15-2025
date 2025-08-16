"""
Mock Data Provider
Provides mock data for testing different scenarios
"""

import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List


class MockDataProvider:
    """Provides mock data for different scenarios"""

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
                    "Electronics-US",
                    "Electronics-EU",
                ],
                "Base Bid": [1.25, 0.95, 2.10, 1.85, 1.50, "Ignore"],
                "Target CPA": [5.00, 4.50, 8.00, 7.50, 6.00, None],
            }
        )

    @staticmethod
    def get_mock_template_missing() -> pd.DataFrame:
        """Get template with missing portfolios"""
        return pd.DataFrame(
            {
                "Portfolio Name": [
                    "Kids-Brand-US",
                    "Kids-Brand-EU",
                    "Supplements-US",
                ],
                "Base Bid": [1.25, 0.95, 2.10],
                "Target CPA": [5.00, 4.50, 8.00],
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
    def get_mock_bulk_data() -> pd.DataFrame:
        """Get mock bulk data with 46 columns"""
        # Create base data
        num_rows = 100

        data = {
            "Product": ["ASIN" + str(i % 20) for i in range(num_rows)],
            "Entity": [
                "Keyword" if i % 2 == 0 else "Product Targeting"
                for i in range(num_rows)
            ],
            "Operation": ["Create"] * num_rows,
            "Campaign ID": ["1234567890"] * num_rows,
            "Ad Group ID": ["9876543210"] * num_rows,
            "Portfolio ID": ["1111111111"] * num_rows,
            "Ad ID": [""] * num_rows,
            "Keyword ID": [""] * num_rows,
            "Product Targeting ID": [""] * num_rows,
            "Campaign Name": ["Campaign-1"] * num_rows,
            "Ad Group Name": ["AdGroup-1"] * num_rows,
            "Campaign Name (Informational only)": ["Campaign-1"] * num_rows,
            "Ad Group Name (Informational only)": ["AdGroup-1"] * num_rows,
            "Portfolio Name (Informational only)": [
                [
                    "Kids-Brand-US",
                    "Kids-Brand-EU",
                    "Supplements-US",
                    "Supplements-EU",
                    "Electronics-US",
                    "Electronics-EU",
                ][i % 6]
                for i in range(num_rows)
            ],
            "Start Date": ["01/01/2024"] * num_rows,
            "End Date": [""] * num_rows,
            "Targeting Type": ["MANUAL"] * num_rows,
            "State": ["enabled"] * 80 + ["paused"] * 20,
            "Campaign State (Informational only)": ["enabled"] * 90 + ["paused"] * 10,
            "Ad Group State (Informational only)": ["enabled"] * 85 + ["paused"] * 15,
            "Daily Budget": [10.00] * num_rows,
            "SKU": [""] * num_rows,
            "ASIN": ["B00" + str(i).zfill(7) for i in range(num_rows)],
            "Eligibility Status (Informational only)": [""] * num_rows,
            "Reason for Ineligibility (Informational only)": [""] * num_rows,
            "Ad Group Default Bid": [1.00] * num_rows,
            "Ad Group Default Bid (Informational only)": [1.00] * num_rows,
            "Bid": [0.50 + (i % 30) * 0.1 for i in range(num_rows)],
            "Keyword Text": ["keyword " + str(i) for i in range(num_rows)],
            "Native Language Keyword": [""] * num_rows,
            "Native Language Locale": [""] * num_rows,
            "Match Type": ["BROAD"] * 50 + ["PHRASE"] * 30 + ["EXACT"] * 20,
            "Bidding Strategy": [""] * num_rows,
            "Placement": [""] * num_rows,
            "Percentage": [""] * num_rows,
            "Product Targeting Expression": [""] * num_rows,
            "Resolved Product Targeting Expression (Informational only)": [""]
            * num_rows,
            "Impressions": [100 + i * 50 for i in range(num_rows)],
            "Clicks": [5 + i % 20 for i in range(num_rows)],
            "Click-through Rate": [0.05 + (i % 10) * 0.01 for i in range(num_rows)],
            "Spend": [10.00 + i * 2 for i in range(num_rows)],
            "Sales": [0 if i % 3 == 0 else 50 + i * 10 for i in range(num_rows)],
            "Orders": [0 if i % 3 == 0 else 1 + i % 5 for i in range(num_rows)],
            "Units": [0 if i % 3 == 0 else 1 + i % 10 for i in range(num_rows)],
            "Conversion Rate": [
                0 if i % 3 == 0 else 0.05 + (i % 20) * 0.01 for i in range(num_rows)
            ],
            "ACOS": [0 if i % 3 == 0 else 20 + i % 80 for i in range(num_rows)],
            "CPC": [0.50 + (i % 20) * 0.05 for i in range(num_rows)],
            "ROAS": [
                0 if i % 3 == 0 else 2.0 + (i % 30) * 0.1 for i in range(num_rows)
            ],
        }

        return pd.DataFrame(data)

    @staticmethod
    def get_cleaned_bulk() -> pd.DataFrame:
        """Get cleaned bulk data (after filtering)"""
        bulk = MockDataProvider.get_mock_bulk_data()

        # Apply cleaning filters
        cleaned = bulk[
            (bulk["Entity"].isin(["Keyword", "Product Targeting"]))
            & (bulk["State"] == "enabled")
            & (bulk["Campaign State (Informational only)"] == "enabled")
            & (bulk["Ad Group State (Informational only)"] == "enabled")
        ]

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
            df = MockDataProvider.get_cleaned_bulk()
            df["Operation"] = "Update"
            df["Bid"] = 0.02  # Simulated optimization

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Clean Zero Sales", index=False)
                df.to_excel(writer, sheet_name="Working Zero Sales", index=False)

        elif file_type == "clean":
            df = MockDataProvider.get_cleaned_bulk()
            df["Operation"] = "Update"
            df["Bid"] = 0.02  # Simulated optimization

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
    def get_processing_stats() -> Dict[str, Any]:
        """Get mock processing statistics"""
        return {
            "rows_processed": 1234,
            "rows_modified": 456,
            "calculation_errors": 7,
            "high_bids": 3,  # > 1.25
            "low_bids": 2,  # < 0.02
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
