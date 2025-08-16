"""
File Generator
Generates Working and Clean output files from processed data
"""

import pandas as pd
from io import BytesIO
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
processors_dir = os.path.dirname(current_dir)
business_dir = os.path.dirname(processors_dir)
project_root = os.path.dirname(business_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.writers.output_writer import OutputWriter
from utils.filename_generator import (
    generate_output_filename,
    get_sheet_name,
    get_file_size_display,
)


class FileGenerator:
    """Generates output files from optimized data"""

    def __init__(self):
        """Initialize file generator"""
        self.output_writer = OutputWriter()
        self.generation_stats = {}

    def generate_output_files(
        self,
        cleaned_bulk_df: pd.DataFrame,
        selected_optimizations: List[str],
        template_df: Optional[pd.DataFrame] = None,
    ) -> Tuple[BytesIO, BytesIO, Dict[str, Any]]:
        """
        Generate both Working and Clean files

        Args:
            cleaned_bulk_df: Cleaned Bulk DataFrame
            selected_optimizations: List of optimization names to apply
            template_df: Template DataFrame (optional, for future optimizations)

        Returns:
            Tuple of (working_file, clean_file, stats)
        """
        # Reset stats
        self.generation_stats = {
            "start_time": datetime.now(),
            "selected_optimizations": selected_optimizations,
            "input_rows": len(cleaned_bulk_df),
            "sheets_created": 0,
            "errors": [],
        }

        # Prepare data for each optimization
        optimizations_data = {}

        for optimization_name in selected_optimizations:
            try:
                # For now, we only have Zero Sales
                # Future optimizations will be added here
                if optimization_name == "Zero Sales":
                    processed_df = self._apply_zero_sales_optimization(cleaned_bulk_df)
                else:
                    # For unimplemented optimizations, use original data
                    processed_df = cleaned_bulk_df.copy()

                # Ensure Operation column is set to Update
                processed_df["Operation"] = "Update"

                # DEBUG: Check columns are preserved
                print(
                    f"DEBUG: Processed DataFrame has {len(processed_df.columns)} columns"
                )

                # Store both clean and working versions
                optimizations_data[optimization_name] = {
                    "clean": processed_df.copy(),
                    "working": processed_df.copy(),  # In future, working might have extra columns
                }

                self.generation_stats["sheets_created"] += 2

            except Exception as e:
                self.generation_stats["errors"].append(
                    f"Error processing {optimization_name}: {str(e)}"
                )
                # Use original data if optimization fails
                fallback_df = cleaned_bulk_df.copy()
                fallback_df["Operation"] = "Update"
                optimizations_data[optimization_name] = {
                    "clean": fallback_df,
                    "working": fallback_df,
                }

        # Generate Working file (Clean + Working sheets)
        working_file = self._generate_working_file(optimizations_data)

        # Generate Clean file (Clean sheets only)
        clean_file = self._generate_clean_file(optimizations_data)

        # Calculate final stats
        self.generation_stats["end_time"] = datetime.now()
        self.generation_stats["duration"] = (
            self.generation_stats["end_time"] - self.generation_stats["start_time"]
        ).total_seconds()

        # Get file stats
        working_stats = self.output_writer.get_file_stats(working_file)
        clean_stats = self.output_writer.get_file_stats(clean_file)

        self.generation_stats["working_file"] = working_stats
        self.generation_stats["clean_file"] = clean_stats

        return working_file, clean_file, self.generation_stats

    def _generate_working_file(
        self, optimizations_data: Dict[str, Dict[str, pd.DataFrame]]
    ) -> BytesIO:
        """
        Generate Working file with both Clean and Working sheets

        Args:
            optimizations_data: Dict with optimization data

        Returns:
            BytesIO buffer with Excel file
        """
        # Create Working file
        working_file = self.output_writer.create_working_file(optimizations_data)

        return working_file

    def _generate_clean_file(
        self, optimizations_data: Dict[str, Dict[str, pd.DataFrame]]
    ) -> BytesIO:
        """
        Generate Clean file with only Clean sheets

        Args:
            optimizations_data: Dict with optimization data

        Returns:
            BytesIO buffer with Excel file
        """
        # Extract only clean DataFrames
        clean_data = {name: data["clean"] for name, data in optimizations_data.items()}

        # Create Clean file
        clean_file = self.output_writer.create_clean_file(clean_data)

        return clean_file

    def _apply_zero_sales_optimization(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply Zero Sales optimization (placeholder for now)
        Real implementation will be in Zero Sales optimization module

        Args:
            df: Input DataFrame with ALL 48 columns from Bulk

        Returns:
            Optimized DataFrame with ALL columns preserved
        """
        # Make a copy to avoid modifying original - KEEPS ALL COLUMNS
        optimized_df = df.copy()

        # DEBUG: Print column info
        print(f"DEBUG: Input DataFrame has {len(optimized_df.columns)} columns")
        print(f"DEBUG: First 5 columns: {list(optimized_df.columns[:5])}")

        # Simple logic: Set Bid to 0.02 for rows with Sales = 0
        if "Sales" in optimized_df.columns and "Bid" in optimized_df.columns:
            zero_sales_mask = optimized_df["Sales"] == 0
            optimized_df.loc[zero_sales_mask, "Bid"] = 0.02

            # Track how many rows were modified
            modified_count = zero_sales_mask.sum()
            self.generation_stats[f"zero_sales_modified"] = modified_count

        # Ensure Operation column is Update (but keep all other columns)
        if "Operation" in optimized_df.columns:
            optimized_df["Operation"] = "Update"

        print(f"DEBUG: Output DataFrame has {len(optimized_df.columns)} columns")

        return optimized_df

    def generate_filenames(self) -> Tuple[str, str]:
        """
        Generate filenames for Working and Clean files

        Returns:
            Tuple of (working_filename, clean_filename)
        """
        working_filename = generate_output_filename("Working")
        clean_filename = generate_output_filename("Clean")

        return working_filename, clean_filename

    def get_generation_summary(self) -> Dict[str, Any]:
        """
        Get summary of file generation

        Returns:
            Dictionary with generation statistics
        """
        summary = self.generation_stats.copy()

        # Add human-readable messages
        messages = []

        if summary.get("sheets_created", 0) > 0:
            messages.append(f"Created {summary['sheets_created']} sheets")

        if "working_file" in summary:
            working_size = get_file_size_display(summary["working_file"]["size_bytes"])
            messages.append(
                f"Working file: {working_size}, {summary['working_file']['sheet_count']} sheets"
            )

        if "clean_file" in summary:
            clean_size = get_file_size_display(summary["clean_file"]["size_bytes"])
            messages.append(
                f"Clean file: {clean_size}, {summary['clean_file']['sheet_count']} sheets"
            )

        if summary.get("errors"):
            messages.append(f"Encountered {len(summary['errors'])} errors")

        summary["messages"] = messages

        return summary

    def validate_output_files(
        self, working_file: BytesIO, clean_file: BytesIO
    ) -> Dict[str, Any]:
        """
        Validate that output files are correct

        Args:
            working_file: Working file buffer
            clean_file: Clean file buffer

        Returns:
            Validation result
        """
        issues = []

        try:
            # Check Working file
            working_file.seek(0)
            working_excel = pd.ExcelFile(working_file)
            working_sheets = working_excel.sheet_names

            # Should have 2 sheets per optimization
            if len(working_sheets) % 2 != 0:
                issues.append(
                    "Working file should have even number of sheets (Clean + Working pairs)"
                )

            # Check Clean file
            clean_file.seek(0)
            clean_excel = pd.ExcelFile(clean_file)
            clean_sheets = clean_excel.sheet_names

            # Clean should have half the sheets of Working
            if len(clean_sheets) * 2 != len(working_sheets):
                issues.append("Clean file should have half the sheets of Working file")

            # Check that all sheets have Operation = Update
            for sheet_name in working_sheets:
                df = pd.read_excel(working_file, sheet_name=sheet_name)
                if "Operation" in df.columns:
                    non_update = df[df["Operation"] != "Update"]
                    if len(non_update) > 0:
                        issues.append(
                            f"Sheet '{sheet_name}' has {len(non_update)} rows without Operation='Update'"
                        )

            # Reset file positions
            working_file.seek(0)
            clean_file.seek(0)

        except Exception as e:
            issues.append(f"Validation error: {str(e)}")

        return {"is_valid": len(issues) == 0, "issues": issues}
