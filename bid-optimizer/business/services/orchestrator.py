"""
Orchestrator Service
Coordinates validation and processing
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
from io import BytesIO
import sys
import os
import traceback

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
business_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(business_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from business.validators import FileValidator, PortfolioValidator
from business.processors import BulkCleaner, FileGenerator
from data.readers import ExcelReader, CSVReader


class Orchestrator:
    """Main orchestrator for validation and processing"""

    def __init__(self):
        """Initialize orchestrator with validators and processors"""
        self.file_validator = FileValidator()
        self.portfolio_validator = PortfolioValidator()
        self.bulk_cleaner = BulkCleaner()
        self.file_generator = FileGenerator()
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

            # Clean Bulk data and separate into sheets
            cleaned_targets_df = self.bulk_cleaner.clean_bulk(bulk_df)
            cleaning_summary = self.bulk_cleaner.get_cleaning_summary()
            result["cleaning_summary"] = cleaning_summary

            # Check if any rows remain after cleaning
            validation_check = self.bulk_cleaner.validate_cleaning_result(
                cleaned_targets_df
            )
            if not validation_check["is_valid"]:
                result["errors"].extend(validation_check["issues"])
                result["warnings"].extend(validation_check["warnings"])
                return result

            # Validate portfolios (only on Targets sheet)
            portfolio_validation = self.portfolio_validator.validate_portfolios(
                template_df, cleaned_targets_df
            )
            result["portfolio_validation"] = portfolio_validation

            # Extract results
            result["missing_portfolios"] = portfolio_validation.get(
                "missing_portfolios", []
            )
            result["ignored_portfolios"] = portfolio_validation.get(
                "ignored_portfolios", []
            )
            result["excess_portfolios"] = portfolio_validation.get(
                "excess_portfolios", []
            )

            # Check for blocking issues
            if portfolio_validation.get("blocks_processing", False):
                result["errors"].extend(portfolio_validation.get("errors", []))
                return result

            # Add warnings
            result["warnings"].extend(portfolio_validation.get("warnings", []))

            # Set stats
            result["stats"] = {
                "template_rows": len(template_df),
                "bulk_rows": len(bulk_df),
                "targets_rows": len(cleaned_targets_df),
                "product_ads_rows": cleaning_summary["stats"].get(
                    "product_ads_final", 0
                ),
                "bidding_adjustments_rows": cleaning_summary["stats"].get(
                    "bidding_adjustments_final", 0
                ),
            }

            # If we got here, validation passed
            result["is_valid"] = True

            # Store the separated dataframes for later use
            result["separated_dataframes"] = (
                self.bulk_cleaner.get_separated_dataframes()
            )
            result["template_df"] = template_df

            return result

        except Exception as e:
            result["errors"].append(f"Unexpected error: {str(e)}")
            print(f"Orchestrator validation error: {e}")
            traceback.print_exc()
            return result

    def process_files(
        self,
        template_df: pd.DataFrame,
        separated_dataframes: Dict[str, pd.DataFrame],
        selected_optimizations: list,
    ) -> Tuple[BytesIO, BytesIO, Dict[str, Any]]:
        """
        Process files with selected optimizations

        Args:
            template_df: Template DataFrame
            separated_dataframes: Dictionary with separated DataFrames
                - targets: Cleaned Targets DataFrame
                - product_ads: Product Ads DataFrame
                - bidding_adjustments: Bidding Adjustments DataFrame
            selected_optimizations: List of optimization names

        Returns:
            Tuple of (working_file, clean_file, stats)
        """
        try:
            # Generate output files with all separated dataframes
            working_file, clean_file, stats = self.file_generator.generate_output_files(
                separated_dataframes=separated_dataframes,
                selected_optimizations=selected_optimizations,
                template_df=template_df,
            )

            return working_file, clean_file, stats

        except Exception as e:
            print(f"Orchestrator processing error: {e}")
            traceback.print_exc()
            raise

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
            print(f"DEBUG: Reading {file_type} file")
            print(f"DEBUG: File type: {type(file)}")

            # Reset file position to beginning
            if hasattr(file, "seek"):
                file.seek(0)

            # Try to read as Excel first
            if file_type == "template":
                df = self.excel_reader.read(file)
            else:  # bulk
                df = self.excel_reader.read(
                    file, sheet_name="Sponsored Products Campaigns"
                )

            print(
                f"DEBUG: Successfully read {file_type} file with {len(df) if df is not None else 0} rows"
            )
            return df

        except Exception as e:
            print(f"ERROR: Failed to read {file_type} file: {e}")
            import traceback

            traceback.print_exc()

            # Try CSV as fallback
            try:
                print(f"DEBUG: Trying to read as CSV")
                file.seek(0)
                df = self.csv_reader.read(file)
                print(f"DEBUG: Successfully read CSV with {len(df)} rows")
                return df
            except Exception as csv_error:
                print(f"ERROR: CSV read also failed: {csv_error}")
                return None
