"""
Orchestrator Service
Coordinates validation and processing
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
from io import BytesIO
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
business_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(business_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from business.validators import FileValidator, PortfolioValidator
from business.processors import BulkCleaner
from data.readers import ExcelReader, CSVReader


class Orchestrator:
    """Main orchestrator for validation and processing"""

    def __init__(self):
        """Initialize orchestrator with validators and processors"""
        self.file_validator = FileValidator()
        self.portfolio_validator = PortfolioValidator()
        self.bulk_cleaner = BulkCleaner()
        self.excel_reader = ExcelReader()
        self.csv_reader = CSVReader()

    def validate_files(
        self, template_file: BytesIO, bulk_file: BytesIO
    ) -> Dict[str, Any]:
        """
        Complete validation of Template and Bulk files

        Args:
            template_file: Template file buffer
            bulk_file: Bulk file buffer

        Returns:
            Complete validation result
        """
        result = {
            "is_valid": False,
            "template_validation": None,
            "bulk_validation": None,
            "portfolio_validation": None,
            "cleaning_summary": None,
            "errors": [],
            "warnings": [],
            "missing_portfolios": [],
            "ignored_portfolios": [],
            "excess_portfolios": [],
            "stats": {},
        }

        try:
            # Read Template file
            template_df = self._read_file(template_file, "template")
            if template_df is None:
                result["errors"].append("Failed to read Template file")
                return result

            # Read Bulk file
            bulk_df = self._read_file(bulk_file, "bulk")
            if bulk_df is None:
                result["errors"].append("Failed to read Bulk file")
                return result

            # Validate Template structure
            template_validation = self.file_validator.validate_template(template_df)
            result["template_validation"] = template_validation

            if not template_validation["is_valid"]:
                result["errors"].extend(template_validation["errors"])
                result["warnings"].extend(template_validation["warnings"])
                return result

            # Validate Bulk structure
            bulk_validation = self.file_validator.validate_bulk(bulk_df)
            result["bulk_validation"] = bulk_validation

            if not bulk_validation["is_valid"]:
                result["errors"].extend(bulk_validation["errors"])
                result["warnings"].extend(bulk_validation["warnings"])
                return result

            # Clean Bulk data
            cleaned_bulk_df = self.bulk_cleaner.clean_bulk(bulk_df)
            cleaning_summary = self.bulk_cleaner.get_cleaning_summary()
            result["cleaning_summary"] = cleaning_summary

            # Check if any rows remain after cleaning
            validation_check = self.bulk_cleaner.validate_cleaning_result(
                cleaned_bulk_df
            )
            if not validation_check["is_valid"]:
                result["errors"].extend(validation_check["issues"])
                result["warnings"].extend(validation_check["warnings"])
                return result

            # Validate portfolios
            portfolio_validation = self.portfolio_validator.validate_portfolios(
                template_df, cleaned_bulk_df
            )
            result["portfolio_validation"] = portfolio_validation

            # Update result with portfolio validation
            result["missing_portfolios"] = portfolio_validation["missing_portfolios"]
            result["ignored_portfolios"] = portfolio_validation["ignored_portfolios"]
            result["excess_portfolios"] = portfolio_validation["excess_portfolios"]

            # Get summary statistics
            portfolio_summary = self.portfolio_validator.get_portfolio_summary(
                template_df, cleaned_bulk_df
            )

            result["stats"] = {
                "original_rows": len(bulk_df),
                "cleaned_rows": len(cleaned_bulk_df),
                "filtered_rows": len(bulk_df) - len(cleaned_bulk_df),
                "template_portfolios": portfolio_summary["template_total"],
                "template_valid": portfolio_summary["template_valid"],
                "template_ignored": portfolio_summary["template_ignored"],
                "bulk_portfolios": portfolio_summary["bulk_unique_portfolios"],
                "missing_count": len(result["missing_portfolios"]),
                "ignored_count": len(result["ignored_portfolios"]),
            }

            # Final validation result
            result["is_valid"] = portfolio_validation["is_valid"]

            # Add all warnings
            result["warnings"].extend(bulk_validation.get("warnings", []))

            # Store DataFrames in result for later use
            result["template_df"] = template_df
            result["bulk_df"] = bulk_df
            result["cleaned_bulk_df"] = cleaned_bulk_df

        except Exception as e:
            result["errors"].append(f"Validation error: {str(e)}")
            result["is_valid"] = False

        return result

    def _read_file(self, file: BytesIO, file_type: str) -> Optional[pd.DataFrame]:
        """
        Read file and return DataFrame

        Args:
            file: File buffer
            file_type: 'template' or 'bulk'

        Returns:
            DataFrame or None if failed
        """
        try:
            # Check file extension from name if available
            file_name = getattr(file, "name", "unknown")

            if file_name.endswith(".xlsx"):
                return self.excel_reader.read(file, file_type)
            elif file_name.endswith(".csv"):
                return self.csv_reader.read(file, file_type)
            else:
                # Try Excel first, then CSV
                try:
                    return self.excel_reader.read(file, file_type)
                except:
                    file.seek(0)  # Reset file pointer
                    return self.csv_reader.read(file, file_type)

        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None
