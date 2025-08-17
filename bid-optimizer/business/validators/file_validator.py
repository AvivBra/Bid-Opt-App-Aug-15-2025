"""
bid-optimizer/business/validators/file_validator.py
File Validator - Validates Template and Bulk file structure and data
"""

import pandas as pd
from typing import Dict, List, Any, Optional


class FileValidator:
    """Validates file structure and basic data requirements"""

    # Template requirements
    TEMPLATE_COLUMNS = ["Portfolio Name", "Base Bid", "Target CPA"]

    # Bulk requirements
    BULK_COLUMNS_COUNT = 48
    BULK_REQUIRED_SHEET = "Sponsored Products Campaigns"

    # File size limits
    MAX_FILE_SIZE_MB = 40
    MAX_ROWS = 500000

    # Bid limits
    MIN_BID = 0.02
    MAX_BID = 999.99

    def __init__(self):
        """Initialize validator"""
        self.errors = []
        self.warnings = []

    def validate_template(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate template file structure and data

        Args:
            df: Template DataFrame

        Returns:
            Validation result dictionary
        """
        self.errors = []
        self.warnings = []

        # Check columns
        if list(df.columns) != self.TEMPLATE_COLUMNS:
            self.errors.append(
                f"Columns must be exactly: {', '.join(self.TEMPLATE_COLUMNS)}"
            )
            return self._create_result(False)

        # Check if empty
        if len(df) == 0:
            self.errors.append("Template has no data rows")
            return self._create_result(False)

        # Validate each row
        for idx, row in df.iterrows():
            row_num = idx + 2  # Excel row number (header is row 1)

            # Check Portfolio Name
            if (
                pd.isna(row["Portfolio Name"])
                or str(row["Portfolio Name"]).strip() == ""
            ):
                self.errors.append(f"Portfolio Name cannot be empty in row {row_num}")

            # Check Base Bid
            base_bid = row["Base Bid"]
            if pd.isna(base_bid):
                self.errors.append(f"Base Bid is required in row {row_num}")
            else:
                # Convert to string and check if it's "ignore" (case-insensitive)
                base_bid_str = str(base_bid).strip().lower()

                if base_bid_str != "ignore":
                    # Try to convert to float
                    try:
                        bid_value = float(base_bid)
                        if bid_value < 0 or bid_value > self.MAX_BID:
                            self.errors.append(
                                f"Base Bid must be between 0.00 and {self.MAX_BID} in row {row_num}"
                            )
                    except (ValueError, TypeError):
                        self.errors.append(
                            f"Invalid Base Bid value in row {row_num} - must be number or 'Ignore'"
                        )

            # Check Target CPA (optional, can be empty)
            target_cpa = row["Target CPA"]
            if not pd.isna(target_cpa) and target_cpa != "":
                try:
                    cpa_value = float(target_cpa)
                    if cpa_value < 0:
                        self.errors.append(
                            f"Target CPA cannot be negative in row {row_num}"
                        )
                except (ValueError, TypeError):
                    self.errors.append(
                        f"Invalid Target CPA value in row {row_num} - must be a number"
                    )

        # Check for duplicate portfolio names
        portfolio_names = df["Portfolio Name"].dropna().astype(str).str.strip()
        duplicates = portfolio_names[portfolio_names.duplicated()].unique()
        if len(duplicates) > 0:
            for dup in duplicates:
                self.errors.append(f"Duplicate portfolio name: {dup}")

        # Check if all portfolios are ignored
        non_ignored_count = 0
        for _, row in df.iterrows():
            base_bid = row["Base Bid"]
            if not pd.isna(base_bid):
                base_bid_str = str(base_bid).strip().lower()
                if base_bid_str != "ignore":
                    non_ignored_count += 1

        if non_ignored_count == 0:
            self.errors.append("All portfolios marked as 'Ignore' - cannot proceed")

        # Add warnings for ignored portfolios
        ignored_count = len(df) - non_ignored_count
        if ignored_count > 0:
            self.warnings.append(
                f"{ignored_count} portfolio(s) marked as 'Ignore' will be skipped"
            )

        return self._create_result(len(self.errors) == 0)

    def validate_bulk(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate bulk file structure

        Args:
            df: Bulk DataFrame

        Returns:
            Validation result dictionary
        """
        self.errors = []
        self.warnings = []

        # Check if DataFrame is empty
        if df is None or len(df) == 0:
            self.errors.append("Bulk file is empty - no data found")
            return self._create_result(False)

        # Check column count
        if len(df.columns) != self.BULK_COLUMNS_COUNT:
            self.errors.append(
                f"Bulk file must have exactly {self.BULK_COLUMNS_COUNT} columns "
                f"(found {len(df.columns)})"
            )
            # Don't continue validation if column count is wrong
            return self._create_result(False)

        # Check row count
        if len(df) > self.MAX_ROWS:
            self.errors.append(
                f"File contains more than {self.MAX_ROWS:,} rows (found: {len(df):,})"
            )
            return self._create_result(False)

        # Check for required columns (Entity is critical)
        if "Entity" not in df.columns:
            self.errors.append("Missing required 'Entity' column")

        # Check for Portfolio Name column
        portfolio_column = "Portfolio Name (Informational only)"
        if portfolio_column not in df.columns:
            self.errors.append(f"Missing required '{portfolio_column}' column")

        # Check for State columns
        state_columns = [
            "State",
            "Campaign State (Informational only)",
            "Ad Group State (Informational only)",
        ]
        for col in state_columns:
            if col not in df.columns:
                self.errors.append(f"Missing required '{col}' column")

        # Add warnings for large files
        if len(df) > 100000:
            self.warnings.append(
                f"Large file detected ({len(df):,} rows) - processing may take longer"
            )

        return self._create_result(len(self.errors) == 0)

    def validate_file_size(self, file_size_bytes: int) -> Dict[str, Any]:
        """
        Validate file size before reading

        Args:
            file_size_bytes: File size in bytes

        Returns:
            Validation result
        """
        self.errors = []
        self.warnings = []

        max_bytes = self.MAX_FILE_SIZE_MB * 1024 * 1024

        if file_size_bytes > max_bytes:
            self.errors.append(
                f"File exceeds {self.MAX_FILE_SIZE_MB}MB limit "
                f"(size: {file_size_bytes / 1024 / 1024:.1f}MB)"
            )
            return self._create_result(False)

        # Warning for large files
        if file_size_bytes > 10 * 1024 * 1024:  # 10MB
            self.warnings.append(
                f"Large file detected ({file_size_bytes / 1024 / 1024:.1f}MB) - "
                "processing may take longer"
            )

        return self._create_result(True)

    def _create_result(self, is_valid: bool) -> Dict[str, Any]:
        """
        Create validation result dictionary

        Args:
            is_valid: Whether validation passed

        Returns:
            Result dictionary
        """
        return {
            "is_valid": is_valid,
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy(),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
        }
