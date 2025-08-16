"""
CSV Reader for Bid Optimizer
Reads CSV files with encoding detection
"""

import pandas as pd
from io import BytesIO, StringIO
from typing import Optional, List
import chardet


class CSVReader:
    """Reads CSV files with automatic encoding detection"""

    # File size limit
    MAX_FILE_SIZE = 40 * 1024 * 1024  # 40MB
    MAX_ROWS = 500000

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
        """Initialize CSV reader"""
        self.errors = []
        self.warnings = []
        self.detected_encoding = None

    def read(
        self, file: BytesIO, file_type: str = "auto", encoding: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Read CSV file and return DataFrame

        Args:
            file: File buffer
            file_type: 'template', 'bulk', or 'auto' (auto-detect)
            encoding: File encoding (optional, will auto-detect if not provided)

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
        file_content = file.getvalue()
        file_size = len(file_content)

        if file_size > self.MAX_FILE_SIZE:
            raise FileSizeError(
                f"File exceeds 40MB limit (size: {file_size / 1024 / 1024:.1f}MB)"
            )

        # Detect encoding if not provided
        if not encoding:
            encoding = self._detect_encoding(file_content)
            self.detected_encoding = encoding

        # Try to read CSV file
        try:
            # Decode bytes to string
            if isinstance(file_content, bytes):
                text_content = file_content.decode(encoding)
            else:
                text_content = file_content

            # Read CSV from string
            df = pd.read_csv(StringIO(text_content))

            # Check if empty
            if df.empty:
                raise EmptyFileError("File contains no data")

            # Auto-detect file type based on columns
            if file_type == "auto":
                if len(df.columns) == len(self.TEMPLATE_COLUMNS):
                    file_type = "template"
                elif len(df.columns) == len(self.BULK_COLUMNS):
                    file_type = "bulk"
                else:
                    # Try to determine by column names
                    if set(self.TEMPLATE_COLUMNS).issubset(set(df.columns)):
                        file_type = "template"
                    elif "Portfolio Name (Informational only)" in df.columns:
                        file_type = "bulk"
                    else:
                        # Default to template for small files
                        file_type = "template" if len(df.columns) <= 5 else "bulk"

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

        except UnicodeDecodeError as e:
            # Try with different encoding
            if encoding != "latin-1":
                self.warnings.append(f"Failed with {encoding}, trying latin-1")
                return self.read(file, file_type, encoding="latin-1")
            raise FileReadError(f"Cannot decode CSV file: {str(e)}")

        except pd.errors.ParserError as e:
            raise FileReadError(f"Cannot parse CSV file: {str(e)}")

        except Exception as e:
            if isinstance(
                e,
                (
                    FileSizeError,
                    EmptyFileError,
                    TooManyRowsError,
                    MissingColumnsError,
                    WrongColumnOrderError,
                ),
            ):
                raise  # Re-raise our custom exceptions
            raise FileReadError(f"Error reading CSV file: {str(e)}")

    def _detect_encoding(self, file_content: bytes) -> str:
        """
        Detect file encoding using chardet

        Args:
            file_content: Raw file bytes

        Returns:
            Detected encoding string
        """
        # Sample first 10KB for encoding detection (faster)
        sample_size = min(10240, len(file_content))
        sample = file_content[:sample_size]

        # Detect encoding
        result = chardet.detect(sample)
        encoding = result.get("encoding", "utf-8")
        confidence = result.get("confidence", 0)

        # If low confidence, default to utf-8
        if confidence < 0.7:
            self.warnings.append(
                f"Low confidence in encoding detection ({confidence:.0%}), using utf-8"
            )
            return "utf-8"

        # Map some common encoding names
        encoding_map = {
            "ascii": "utf-8",
            "ISO-8859-1": "latin-1",
            "Windows-1252": "cp1252",
        }

        return encoding_map.get(encoding, encoding).lower()

    def _validate_template_columns(self, df: pd.DataFrame):
        """Validate Template file columns"""
        if list(df.columns) != self.TEMPLATE_COLUMNS:
            # Check if columns exist but in wrong order
            if set(df.columns) == set(self.TEMPLATE_COLUMNS):
                raise WrongColumnOrderError(
                    f"Columns must be exactly in order: {', '.join(self.TEMPLATE_COLUMNS)}"
                )

            # Check for missing columns
            missing = set(self.TEMPLATE_COLUMNS) - set(df.columns)
            if missing:
                raise MissingColumnsError(
                    f"Missing required columns: {', '.join(missing)}"
                )

            # Check for extra columns
            extra = set(df.columns) - set(self.TEMPLATE_COLUMNS)
            if extra:
                raise MissingColumnsError(
                    f"Template must have exactly 3 columns. Extra columns found: {', '.join(list(extra)[:3])}"
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

    def validate_file_size(self, file: BytesIO) -> bool:
        """Check if file size is within limits"""
        file_size = len(file.getvalue())
        return file_size <= self.MAX_FILE_SIZE

    def get_encoding_info(self) -> Optional[str]:
        """Get detected encoding from last read operation"""
        return self.detected_encoding


# Custom Exceptions (same as Excel reader for consistency)
class FileReadError(Exception):
    """Raised when file cannot be read"""

    pass


class FileSizeError(Exception):
    """Raised when file exceeds size limit"""

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
