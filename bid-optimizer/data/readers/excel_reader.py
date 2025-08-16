"""
Excel Reader for Bid Optimizer
Reads real Excel files for Template and Bulk data
"""

import pandas as pd
from io import BytesIO
from typing import Optional, List, Dict, Any
import openpyxl


class ExcelReader:
    """Reads Excel files with support for Template and Bulk formats"""

    # File size limit
    MAX_FILE_SIZE = 40 * 1024 * 1024  # 40MB
    MAX_ROWS = 500000

    # Required sheet for Bulk files
    BULK_SHEET_NAME = "Sponsored Products Campaigns"

    # Required columns for Template
    TEMPLATE_COLUMNS = ["Portfolio Name", "Base Bid", "Target CPA"]

    # Required columns for Bulk (46 columns)
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

    def __init__(self):
        """Initialize Excel reader"""
        self.errors = []
        self.warnings = []

    def read(
        self, file: BytesIO, file_type: str = "auto", sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Read Excel file and return DataFrame

        Args:
            file: File buffer
            file_type: 'template', 'bulk', or 'auto' (auto-detect)
            sheet_name: Specific sheet to read (optional)

        Returns:
            DataFrame with file contents

        Raises:
            FileReadError: If file cannot be read
            ValidationError: If file structure is invalid
        """
        # Reset errors and warnings
        self.errors = []
        self.warnings = []

        # Check file size
        file_size = len(file.getvalue())
        if file_size > self.MAX_FILE_SIZE:
            raise FileSizeError(
                f"File exceeds 40MB limit (size: {file_size / 1024 / 1024:.1f}MB)"
            )

        # Try to read Excel file
        try:
            # Get all sheet names first
            excel_file = pd.ExcelFile(file)
            available_sheets = excel_file.sheet_names

            # Determine which sheet to read
            if file_type == "bulk":
                # For Bulk files, must have specific sheet
                if self.BULK_SHEET_NAME not in available_sheets:
                    raise SheetNotFoundError(
                        f"Required sheet '{self.BULK_SHEET_NAME}' not found. "
                        f"Available sheets: {', '.join(available_sheets)}"
                    )
                sheet_to_read = self.BULK_SHEET_NAME

            elif file_type == "template":
                # For Template files, read first sheet or specified sheet
                if sheet_name and sheet_name in available_sheets:
                    sheet_to_read = sheet_name
                else:
                    sheet_to_read = available_sheets[0]

            else:  # auto-detect
                # Check if it's a Bulk file by looking for the required sheet
                if self.BULK_SHEET_NAME in available_sheets:
                    sheet_to_read = self.BULK_SHEET_NAME
                    file_type = "bulk"
                else:
                    # Assume it's a Template file
                    sheet_to_read = available_sheets[0]
                    file_type = "template"

            # Read the selected sheet
            df = pd.read_excel(file, sheet_name=sheet_to_read)

            # Check if empty
            if df.empty:
                raise EmptyFileError("File contains no data")

            # Check row count for Bulk files
            if file_type == "bulk" and len(df) > self.MAX_ROWS:
                raise TooManyRowsError(
                    f"File contains {len(df):,} rows, maximum is {self.MAX_ROWS:,}"
                )

            # Validate columns based on file type
            if file_type == "template":
                self._validate_template_columns(df)
            elif file_type == "bulk":
                self._validate_bulk_columns(df)

            return df

        except pd.errors.ParserError as e:
            raise FileReadError(f"Cannot read Excel file: {str(e)}")
        except Exception as e:
            if isinstance(
                e,
                (
                    FileSizeError,
                    SheetNotFoundError,
                    EmptyFileError,
                    TooManyRowsError,
                    MissingColumnsError,
                ),
            ):
                raise  # Re-raise our custom exceptions
            raise FileReadError(f"Error reading file: {str(e)}")

    def _validate_template_columns(self, df: pd.DataFrame):
        """Validate Template file columns"""
        if list(df.columns) != self.TEMPLATE_COLUMNS:
            missing = set(self.TEMPLATE_COLUMNS) - set(df.columns)
            extra = set(df.columns) - set(self.TEMPLATE_COLUMNS)

            if missing:
                raise MissingColumnsError(
                    f"Missing required columns: {', '.join(missing)}"
                )
            if extra or list(df.columns) != self.TEMPLATE_COLUMNS:
                raise WrongColumnOrderError(
                    f"Columns must be exactly in order: {', '.join(self.TEMPLATE_COLUMNS)}"
                )

    def _validate_bulk_columns(self, df: pd.DataFrame):
        """Validate Bulk file columns"""
        if len(df.columns) != len(self.BULK_COLUMNS):
            raise MissingColumnsError(
                f"Bulk file must have exactly {len(self.BULK_COLUMNS)} columns, "
                f"found {len(df.columns)}"
            )

        # Check if all required columns exist
        if list(df.columns) != self.BULK_COLUMNS:
            missing = set(self.BULK_COLUMNS) - set(df.columns)
            if missing:
                # Show first 5 missing columns to avoid huge error messages
                missing_list = list(missing)[:5]
                more = f" and {len(missing) - 5} more" if len(missing) > 5 else ""
                raise MissingColumnsError(
                    f"Missing required columns: {', '.join(missing_list)}{more}"
                )

    def get_sheet_names(self, file: BytesIO) -> List[str]:
        """Get list of sheet names in Excel file"""
        try:
            excel_file = pd.ExcelFile(file)
            return excel_file.sheet_names
        except Exception as e:
            raise FileReadError(f"Cannot read sheet names: {str(e)}")

    def validate_file_size(self, file: BytesIO) -> bool:
        """Check if file size is within limits"""
        file_size = len(file.getvalue())
        return file_size <= self.MAX_FILE_SIZE


# Custom Exceptions
class FileReadError(Exception):
    """Raised when file cannot be read"""

    pass


class FileSizeError(Exception):
    """Raised when file exceeds size limit"""

    pass


class SheetNotFoundError(Exception):
    """Raised when required sheet is not found"""

    pass


class EmptyFileError(Exception):
    """Raised when file is empty"""

    pass


class TooManyRowsError(Exception):
    """Raised when file has too many rows"""

    pass


class MissingColumnsError(Exception):
    """Raised when required columns are missing"""

    pass


class WrongColumnOrderError(Exception):
    """Raised when columns are in wrong order"""

    pass
