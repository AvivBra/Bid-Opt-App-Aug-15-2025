"""
Mock Test Scenarios
תרחישי בדיקה מוגדרים מראש
"""

import pandas as pd
from typing import Dict, Tuple, Any
from io import BytesIO
from .mock_template import MockTemplateData
from .mock_bulk import MockBulkData


class MockScenarios:
    """Predefined test scenarios for the application"""

    @staticmethod
    def get_valid_scenario() -> Dict[str, Any]:
        """
        תרחיש תקין - הכל עובד מושלם
        All portfolios match, ready to process
        """
        portfolios = [
            "Kids-Brand-US",
            "Kids-Brand-EU",
            "Supplements-US",
            "Supplements-EU",
        ]

        template_df = MockTemplateData.get_valid_template()
        bulk_df = MockBulkData.generate_bulk_data(100, portfolios)
        cleaned_df = MockBulkData.get_cleaned_bulk(bulk_df)

        return {
            "name": "Valid - All Portfolios Match",
            "template_df": template_df,
            "bulk_df": bulk_df,
            "cleaned_df": cleaned_df,
            "validation_result": {
                "is_valid": True,
                "missing_portfolios": [],
                "excess_portfolios": [],
                "ignored_portfolios": [],
                "messages": ["✓ All portfolios valid"],
                "errors": [],
            },
            "expected_state": "ready",
            "can_process": True,
            "stats": {
                "template_portfolios": 4,
                "bulk_portfolios": 4,
                "original_rows": 100,
                "cleaned_rows": len(cleaned_df),
                "filtered_out": 100 - len(cleaned_df),
            },
        }

    @staticmethod
    def get_missing_scenario() -> Dict[str, Any]:
        """
        תרחיש חסרים - 2 פורטפוליוז חסרים בטמפלייט
        Missing portfolios in template
        """
        # Template has only 2 portfolios
        template_df = MockTemplateData.get_missing_template()

        # Bulk has 4 portfolios
        portfolios = [
            "Kids-Brand-US",
            "Kids-Brand-EU",
            "Supplements-US",
            "Supplements-EU",
        ]
        bulk_df = MockBulkData.generate_bulk_data(100, portfolios)
        cleaned_df = MockBulkData.get_cleaned_bulk(bulk_df)

        # Extract missing portfolios
        template_ports = set(template_df["Portfolio Name"].tolist())
        bulk_ports = set(cleaned_df["Portfolio Name (Informational only)"].unique())
        missing = list(bulk_ports - template_ports)

        return {
            "name": "Missing - 2 Portfolios Missing",
            "template_df": template_df,
            "bulk_df": bulk_df,
            "cleaned_df": cleaned_df,
            "validation_result": {
                "is_valid": False,
                "missing_portfolios": missing,
                "excess_portfolios": [],
                "ignored_portfolios": [],
                "messages": ["❌ Missing portfolios found"],
                "errors": [f"Missing portfolios: {', '.join(missing)}"],
            },
            "expected_state": "validation_failed",
            "can_process": False,
            "stats": {
                "template_portfolios": 2,
                "bulk_portfolios": 4,
                "missing_count": 2,
                "original_rows": 100,
                "cleaned_rows": len(cleaned_df),
            },
        }

    @staticmethod
    def get_excess_scenario() -> Dict[str, Any]:
        """
        תרחיש עודף - 2 פורטפוליוז מיותרים בטמפלייט
        Excess portfolios in template
        """
        # Template has 6 portfolios
        template_df = MockTemplateData.get_excess_template()

        # Bulk has only 4 portfolios
        portfolios = [
            "Kids-Brand-US",
            "Kids-Brand-EU",
            "Supplements-US",
            "Supplements-EU",
        ]
        bulk_df = MockBulkData.generate_bulk_data(100, portfolios)
        cleaned_df = MockBulkData.get_cleaned_bulk(bulk_df)

        # Extract excess portfolios
        template_ports = set(template_df["Portfolio Name"].tolist())
        bulk_ports = set(cleaned_df["Portfolio Name (Informational only)"].unique())
        excess = list(template_ports - bulk_ports)

        return {
            "name": "Excess - 2 Extra Portfolios",
            "template_df": template_df,
            "bulk_df": bulk_df,
            "cleaned_df": cleaned_df,
            "validation_result": {
                "is_valid": True,  # Excess doesn't block processing
                "missing_portfolios": [],
                "excess_portfolios": excess,
                "ignored_portfolios": [],
                "messages": ["⚠️ Excess portfolios in template"],
                "errors": [],
            },
            "expected_state": "ready",
            "can_process": True,
            "stats": {
                "template_portfolios": 6,
                "bulk_portfolios": 4,
                "excess_count": 2,
                "original_rows": 100,
                "cleaned_rows": len(cleaned_df),
            },
        }

    @staticmethod
    def get_mixed_scenario() -> Dict[str, Any]:
        """
        תרחיש מעורב - חסרים + עודפים + Ignore
        Mixed issues: missing, excess, and ignored
        """
        # Template with mixed issues
        template_df = MockTemplateData.get_mixed_template()

        # Bulk has standard 4 portfolios
        portfolios = [
            "Kids-Brand-US",
            "Kids-Brand-EU",
            "Supplements-US",
            "Supplements-EU",
        ]
        bulk_df = MockBulkData.generate_bulk_data(120, portfolios)
        cleaned_df = MockBulkData.get_cleaned_bulk(bulk_df)

        # Extract issues
        template_ports = set(
            template_df[template_df["Base Bid"] != "Ignore"]["Portfolio Name"].tolist()
        )
        bulk_ports = set(cleaned_df["Portfolio Name (Informational only)"].unique())

        missing = ["Supplements-EU"]  # In bulk but not in template (non-ignored)
        excess = ["Electronics-US", "NewProduct-US"]  # In template but not in bulk
        ignored = ["Supplements-US"]  # Has Ignore in template

        return {
            "name": "Mixed - Multiple Issues",
            "template_df": template_df,
            "bulk_df": bulk_df,
            "cleaned_df": cleaned_df,
            "validation_result": {
                "is_valid": False,  # Missing portfolios block processing
                "missing_portfolios": missing,
                "excess_portfolios": excess,
                "ignored_portfolios": ignored,
                "messages": ["❌ Portfolio mismatch found"],
                "errors": [
                    f"Missing portfolios: {', '.join(missing)}",
                    f"Ignored portfolios: {', '.join(ignored)}",
                ],
            },
            "expected_state": "validation_failed",
            "can_process": False,
            "stats": {
                "template_portfolios": 5,
                "bulk_portfolios": 4,
                "missing_count": 1,
                "excess_count": 2,
                "ignored_count": 1,
                "original_rows": 120,
                "cleaned_rows": len(cleaned_df),
            },
        }

    @staticmethod
    def get_edge_case_scenario() -> Dict[str, Any]:
        """
        תרחיש קיצוני - ערכים מיוחדים
        Edge cases with special values
        """
        template_df = MockTemplateData.get_edge_case_template()

        # Bulk with special portfolio names
        portfolios = [
            "Port-With-Special#Chars@",
            "פורטפוליו-בעברית",
            "Very-Long-Portfolio-Name-That-Exceeds-Normal-Length",
            "Normal-Portfolio",
        ]
        bulk_df = MockBulkData.generate_bulk_data(50, portfolios)
        cleaned_df = MockBulkData.get_cleaned_bulk(bulk_df)

        return {
            "name": "Edge Cases - Special Values",
            "template_df": template_df,
            "bulk_df": bulk_df,
            "cleaned_df": cleaned_df,
            "validation_result": {
                "is_valid": True,
                "missing_portfolios": [],
                "excess_portfolios": [],
                "ignored_portfolios": [
                    "Very-Long-Portfolio-Name-That-Exceeds-Normal-Length"
                ],
                "messages": ["⚠️ Special characters in portfolio names"],
                "errors": [],
            },
            "expected_state": "ready",
            "can_process": True,
            "stats": {
                "template_portfolios": 4,
                "bulk_portfolios": 4,
                "special_chars": True,
                "unicode_names": True,
                "min_bid": 0.02,
                "max_bid": 999.99,
            },
        }

    @staticmethod
    def get_large_data_scenario() -> Dict[str, Any]:
        """
        תרחיש נתונים גדולים - 10K שורות
        Large data for performance testing
        """
        portfolios = ["Portfolio-" + str(i) for i in range(20)]

        # Large template
        template_data = {
            "Portfolio Name": portfolios,
            "Base Bid": [1.25] * 20,
            "Target CPA": [5.00] * 20,
        }
        template_df = pd.DataFrame(template_data)

        # Large bulk
        bulk_df = MockBulkData.generate_bulk_data(10000, portfolios)
        cleaned_df = MockBulkData.get_cleaned_bulk(bulk_df)

        return {
            "name": "Large Data - 10K Rows",
            "template_df": template_df,
            "bulk_df": bulk_df,
            "cleaned_df": cleaned_df,
            "validation_result": {
                "is_valid": True,
                "missing_portfolios": [],
                "excess_portfolios": [],
                "ignored_portfolios": [],
                "messages": ["✓ All portfolios valid (large dataset)"],
                "errors": [],
            },
            "expected_state": "ready",
            "can_process": True,
            "stats": {
                "template_portfolios": 20,
                "bulk_portfolios": 20,
                "original_rows": 10000,
                "cleaned_rows": len(cleaned_df),
                "file_size_mb": 23.0,
            },
        }

    @staticmethod
    def get_all_scenarios() -> Dict[str, Dict[str, Any]]:
        """
        Get all predefined scenarios

        Returns:
            Dictionary of all scenarios
        """
        return {
            "valid": MockScenarios.get_valid_scenario(),
            "missing": MockScenarios.get_missing_scenario(),
            "excess": MockScenarios.get_excess_scenario(),
            "mixed": MockScenarios.get_mixed_scenario(),
            "edge": MockScenarios.get_edge_case_scenario(),
            "large": MockScenarios.get_large_data_scenario(),
        }

    @staticmethod
    def create_scenario_files(scenario_name: str) -> Tuple[BytesIO, BytesIO]:
        """
        Create Excel files for a specific scenario

        Args:
            scenario_name: Name of scenario

        Returns:
            Tuple of (template_file, bulk_file) as BytesIO objects
        """
        scenarios = MockScenarios.get_all_scenarios()
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
    def get_scenario_description(scenario_name: str) -> str:
        """
        Get human-readable description of scenario

        Args:
            scenario_name: Name of scenario

        Returns:
            Description string
        """
        descriptions = {
            "valid": "✅ תרחיש תקין - כל הפורטפוליוז תואמים",
            "missing": "❌ תרחיש חסרים - 2 פורטפוליוז חסרים בטמפלייט",
            "excess": "⚠️ תרחיש עודף - 2 פורטפוליוז מיותרים בטמפלייט",
            "mixed": "❌ תרחיש מעורב - בעיות מרובות",
            "edge": "🔧 תרחיש קיצוני - תווים מיוחדים וערכי קצה",
            "large": "📊 תרחיש גדול - 10,000 שורות",
        }
        return descriptions.get(scenario_name, "Unknown scenario")
