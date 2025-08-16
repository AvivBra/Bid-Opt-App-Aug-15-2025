"""
Output Writer
Writes optimized data to Excel files with proper formatting
"""

import pandas as pd
from io import BytesIO
from typing import Dict, Any, Optional
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter


class OutputWriter:
    """Handles writing output Excel files"""

    # Define ID columns that should be formatted as text
    ID_COLUMNS = [
        "Campaign ID",
        "Ad Group ID",
        "Portfolio ID",
        "Ad ID",
        "Keyword ID",
        "Product Targeting ID",
    ]

    # Define uniform column width
    UNIFORM_COLUMN_WIDTH = 15  # Set all columns to same width

    def __init__(self):
        """Initialize output writer"""
        self.pink_fill = PatternFill(
            start_color="FFE4E1", end_color="FFE4E1", fill_type="solid"
        )

    def create_excel_file(self, sheets_data: Dict[str, pd.DataFrame]) -> BytesIO:
        """
        Create Excel file with multiple sheets

        Args:
            sheets_data: Dictionary mapping sheet names to DataFrames

        Returns:
            BytesIO buffer containing the Excel file
        """
        output = BytesIO()

        # Format DataFrames
        sheets_data_formatted = {}
        for sheet_name, df in sheets_data.items():
            df_copy = df.copy()

            # Convert ID columns to string to prevent scientific notation
            for col in self.ID_COLUMNS:
                if col in df_copy.columns:
                    # For ID columns, only convert non-empty values to string
                    mask = df_copy[col] != ""
                    df_copy.loc[mask, col] = df_copy.loc[mask, col].astype(str)
                    # Remove any .0 from the end if it exists
                    df_copy.loc[mask, col] = df_copy.loc[mask, col].str.replace(
                        r"\.0$", "", regex=True
                    )

            # Ensure Operation column is set to "Update"
            if "Operation" in df_copy.columns:
                df_copy["Operation"] = "Update"

            sheets_data_formatted[sheet_name] = df_copy

        # Create Excel writer with specific options
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for sheet_name, df in sheets_data_formatted.items():
                # Write DataFrame to sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Get the worksheet for additional formatting
                worksheet = writer.sheets[sheet_name]

                # Apply additional formatting
                self._format_worksheet(worksheet, df)

        # Reset buffer position
        output.seek(0)

        return output

    def create_working_file(self, sheets_dict: Dict[str, pd.DataFrame]) -> BytesIO:
        """
        Create Working file with all sheets

        Args:
            sheets_dict: Dictionary of sheet_name: DataFrame

        Returns:
            BytesIO buffer containing the Working Excel file
        """
        return self.create_excel_file(sheets_dict)

    def create_clean_file(self, sheets_dict: Dict[str, pd.DataFrame]) -> BytesIO:
        """
        Create Clean file with all sheets

        Args:
            sheets_dict: Dictionary of sheet_name: DataFrame

        Returns:
            BytesIO buffer containing the Clean Excel file
        """
        return self.create_excel_file(sheets_dict)

    def _format_worksheet(self, worksheet, df):
        """
        Apply formatting to worksheet

        Args:
            worksheet: Openpyxl worksheet object
            df: DataFrame for reference
        """
        # Set uniform column width for ALL columns
        for col_idx in range(1, len(df.columns) + 1):
            column_letter = get_column_letter(col_idx)
            worksheet.column_dimensions[column_letter].width = self.UNIFORM_COLUMN_WIDTH

        # Format header row
        for cell in worksheet[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Apply pink highlighting for bid violations if Bid column exists
        if "Bid" in df.columns:
            bid_col_idx = df.columns.get_loc("Bid") + 1  # Excel is 1-indexed
            bid_col_letter = get_column_letter(bid_col_idx)

            for row_idx in range(2, len(df) + 2):  # Skip header, Excel is 1-indexed
                cell = worksheet[f"{bid_col_letter}{row_idx}"]
                try:
                    bid_value = float(cell.value) if cell.value else 0
                    # Highlight if bid is out of range
                    if bid_value < 0.02 or bid_value > 1.25:
                        for col_idx in range(1, len(df.columns) + 1):
                            worksheet.cell(
                                row=row_idx, column=col_idx
                            ).fill = self.pink_fill
                except (ValueError, TypeError):
                    # If bid value is not a number, highlight the row
                    for col_idx in range(1, len(df.columns) + 1):
                        worksheet.cell(
                            row=row_idx, column=col_idx
                        ).fill = self.pink_fill

        # Format ID columns as text to prevent Excel from converting to numbers
        for col_name in self.ID_COLUMNS:
            if col_name in df.columns:
                col_idx = df.columns.get_loc(col_name) + 1
                col_letter = get_column_letter(col_idx)
                for row_idx in range(2, len(df) + 2):
                    cell = worksheet[f"{col_letter}{row_idx}"]
                    if cell.value:
                        cell.number_format = "@"  # Text format

        # Set alignment for all cells
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    def get_file_stats(self, file_buffer: BytesIO) -> Dict[str, Any]:
        """
        Get statistics about the generated file

        Args:
            file_buffer: BytesIO buffer containing Excel file

        Returns:
            Dictionary with file statistics
        """
        # Get file size
        file_buffer.seek(0, 2)  # Seek to end
        size_bytes = file_buffer.tell()
        file_buffer.seek(0)  # Reset position

        # Load workbook to count sheets
        workbook = openpyxl.load_workbook(file_buffer, read_only=True)
        sheet_count = len(workbook.sheetnames)
        sheet_names = workbook.sheetnames
        workbook.close()

        # Reset buffer position
        file_buffer.seek(0)

        return {
            "size_bytes": size_bytes,
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "sheet_count": sheet_count,
            "sheet_names": sheet_names,
        }
