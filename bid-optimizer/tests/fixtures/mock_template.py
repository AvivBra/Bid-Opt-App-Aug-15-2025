"""
Mock Template Data
נתוני דמה לקובץ Template עבור בדיקות
"""

import pandas as pd
from typing import Dict, List
from io import BytesIO


class MockTemplateData:
    """Mock template data for different test scenarios"""

    @staticmethod
    def get_valid_template() -> pd.DataFrame:
        """
        תרחיש תקין - כל הפורטפוליוז קיימים
        4 portfolios with valid Base Bid values
        """
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
    def get_missing_template() -> pd.DataFrame:
        """
        תרחיש חסר - רק 2 פורטפוליוז מתוך 4
        Missing 2 portfolios that exist in bulk
        """
        return pd.DataFrame(
            {
                "Portfolio Name": ["Kids-Brand-US", "Kids-Brand-EU"],
                "Base Bid": [1.25, 0.95],
                "Target CPA": [5.00, 4.50],
            }
        )

    @staticmethod
    def get_excess_template() -> pd.DataFrame:
        """
        תרחיש עודף - 6 פורטפוליוז כש-Bulk מכיל רק 4
        Has 2 extra portfolios not in bulk
        """
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
    def get_mixed_template() -> pd.DataFrame:
        """
        תרחיש מעורב - חלק חסר, חלק עודף, חלק עם Ignore
        Mixed scenario with missing, excess, and ignored
        """
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
    def get_edge_case_template() -> pd.DataFrame:
        """
        תרחיש קיצוני - ערכים מיוחדים
        Edge cases with special values
        """
        return pd.DataFrame(
            {
                "Portfolio Name": [
                    "Port-With-Special#Chars@",
                    "פורטפוליו-בעברית",
                    "Very-Long-Portfolio-Name-That-Exceeds-Normal-Length",
                    "Normal-Portfolio",
                ],
                "Base Bid": [0.02, 999.99, "Ignore", 1.25],  # Min, Max, Ignore
                "Target CPA": [0.01, 9999.99, None, 5.00],
            }
        )

    @staticmethod
    def get_all_ignore_template() -> pd.DataFrame:
        """
        תרחיש שגיאה - כל הפורטפוליוז עם Ignore
        All portfolios set to Ignore - should fail
        """
        return pd.DataFrame(
            {
                "Portfolio Name": ["Kids-Brand-US", "Kids-Brand-EU", "Supplements-US"],
                "Base Bid": ["Ignore", "Ignore", "Ignore"],
                "Target CPA": [None, None, None],
            }
        )

    @staticmethod
    def get_invalid_structure_template() -> pd.DataFrame:
        """
        תרחיש שגיאה - מבנה שגוי
        Wrong column structure
        """
        return pd.DataFrame(
            {
                "Portfolio": ["Port1"],  # Wrong column name
                "Bid": [1.25],  # Wrong column name
                "CPA": [5.00],  # Wrong column name
            }
        )

    @staticmethod
    def get_empty_template() -> pd.DataFrame:
        """
        תרחיש שגיאה - קובץ ריק
        Empty file with headers only
        """
        return pd.DataFrame(columns=["Portfolio Name", "Base Bid", "Target CPA"])

    @staticmethod
    def create_template_file(scenario: str = "valid") -> BytesIO:
        """
        Create Excel file for given scenario

        Args:
            scenario: One of 'valid', 'missing', 'excess', 'mixed', 'edge', 'all_ignore', 'invalid', 'empty'

        Returns:
            BytesIO object containing Excel file
        """
        scenario_map = {
            "valid": MockTemplateData.get_valid_template,
            "missing": MockTemplateData.get_missing_template,
            "excess": MockTemplateData.get_excess_template,
            "mixed": MockTemplateData.get_mixed_template,
            "edge": MockTemplateData.get_edge_case_template,
            "all_ignore": MockTemplateData.get_all_ignore_template,
            "invalid": MockTemplateData.get_invalid_structure_template,
            "empty": MockTemplateData.get_empty_template,
        }

        df = scenario_map.get(scenario, MockTemplateData.get_valid_template)()

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Template", index=False)

        output.seek(0)
        return output

    @staticmethod
    def get_template_stats(df: pd.DataFrame) -> Dict:
        """
        Get statistics about template

        Returns:
            Dictionary with template statistics
        """
        return {
            "total_portfolios": len(df),
            "valid_bids": len(df[df["Base Bid"] != "Ignore"])
            if "Base Bid" in df.columns
            else 0,
            "ignored": len(df[df["Base Bid"] == "Ignore"])
            if "Base Bid" in df.columns
            else 0,
            "has_target_cpa": df["Target CPA"].notna().sum()
            if "Target CPA" in df.columns
            else 0,
            "file_size_kb": 125,  # Mock size
        }
