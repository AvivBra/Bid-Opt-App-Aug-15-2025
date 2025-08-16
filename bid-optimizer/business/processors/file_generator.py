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
from business.optimizations import get_optimization


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
            "warnings": [],
        }

        # Collect all sheets from all optimizations
        all_working_sheets = {}
        all_clean_sheets = {}

        for optimization_name in selected_optimizations:
            try:
                # Get the optimization instance
                optimization = get_optimization(optimization_name)

                # Apply the optimization
                optimized_sheets, stats = optimization.optimize(
                    cleaned_bulk_df, template_df
                )

                print(
                    f"DEBUG FileGen: Optimization {optimization_name} returned {len(optimized_sheets)} sheets"
                )
                print(f"DEBUG FileGen: Sheet names: {list(optimized_sheets.keys())}")

                # Add stats to generation stats
                if stats.get("warning_messages"):
                    self.generation_stats["warnings"].extend(stats["warning_messages"])
                if stats.get("error_messages"):
                    self.generation_stats["errors"].extend(stats["error_messages"])

                # Process returned sheets
                for sheet_name, df in optimized_sheets.items():
                    print(
                        f"DEBUG FileGen: Processing sheet {sheet_name} with {len(df)} rows, {len(df.columns)} columns"
                    )

                    # Ensure Operation column is set to Update
                    if "Operation" in df.columns:
                        df["Operation"] = "Update"

                    # Add to appropriate collection
                    if "Working" in sheet_name:
                        all_working_sheets[sheet_name] = df
                    else:
                        # Add to both clean and working collections
                        all_clean_sheets[sheet_name] = df
                        # If no specific Working version, create one
                        if f"Working {optimization_name}" not in optimized_sheets:
                            all_working_sheets[f"Working {optimization_name}"] = (
                                df.copy()
                            )

                self.generation_stats["sheets_created"] += len(optimized_sheets)

            except Exception as e:
                self.generation_stats["errors"].append(
                    f"Error processing {optimization_name}: {str(e)}"
                )
                # Use original data if optimization fails
                fallback_df = cleaned_bulk_df.copy()
                fallback_df["Operation"] = "Update"
                all_clean_sheets[f"Clean {optimization_name}"] = fallback_df
                all_working_sheets[f"Working {optimization_name}"] = fallback_df

        # Generate Working file (all sheets)
        working_file = self.output_writer.create_working_file(all_working_sheets)

        # Generate Clean file (clean sheets only)
        clean_file = self.output_writer.create_clean_file(all_clean_sheets)

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

        # Add warnings
        if summary.get("warnings"):
            for warning in summary["warnings"]:
                messages.append(warning)

        if summary.get("errors"):
            messages.append(f"Errors: {len(summary['errors'])}")

        summary["messages"] = messages

        return summary
