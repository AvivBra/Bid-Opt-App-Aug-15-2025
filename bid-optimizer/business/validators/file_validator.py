"""
File Validator
Validates Template and Bulk file structure and data
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
                    try:
                        bid_value = float(base_bid)
                        if bid_value < 0 or bid_value > self.MAX_BID:
                            self.errors.append(
                                f"Base Bid must be between 0 and {self.MAX_BID} in row {row_num}"
                            )
                    except (ValueError, TypeError):
                        self.errors.append(
                            f"Invalid Base Bid value in row {row_num} - must be number or 'Ignore'"
                        )

            # Check Target CPA (optional)
            target_cpa = row["Target CPA"]
            if pd.notna(target_cpa) and target_cpa != "":
                try:
                    cpa_value = float(target_cpa)
                    if cpa_value < 0:
                        self.warnings.append(
                            f"Target CPA should be positive in row {row_num}"
                        )
                except (ValueError, TypeError):
                    self.warnings.append(f"Invalid Target CPA value in row {row_num}")

        # Check for duplicate portfolio names
        portfolio_names = df["Portfolio Name"].dropna()
        duplicates = portfolio_names[portfolio_names.duplicated()].unique()
        if len(duplicates) > 0:
            self.errors.append(f"Duplicate portfolio names: {', '.join(duplicates)}")

        # Check if all portfolios are ignored (now case-insensitive)
        non_ignored = df[df["Base Bid"].astype(str).str.strip().str.lower() != "ignore"]
        if len(non_ignored) == 0:
            self.errors.append("All portfolios marked as 'Ignore' - cannot proceed")

        # Check for special characters (warning only)
        for name in portfolio_names:
            if any(char in str(name) for char in ["#", "@", "&", "%"]):
                self.warnings.append(
                    f"Portfolio name contains special characters: {name}"
                )
                break

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

        # Check column count
        if len(df.columns) != self.BULK_COLUMNS_COUNT:
            self.errors.append(
                f"Bulk file must have exactly {self.BULK_COLUMNS_COUNT} columns, found {len(df.columns)}"
            )
            return self._create_result(False)

        # Check if empty
        if len(df) == 0:
            self.errors.append("Bulk file has no data rows")
            return self._create_result(False)

        # Check row count
        if len(df) > self.MAX_ROWS:
            self.errors.append(
                f"File contains more than {self.MAX_ROWS:,} rows (found: {len(df):,})"
            )
            return self._create_result(False)

        # Check for required columns (by position)
        required_column_checks = {
            1: "Entity",  # Column B
            2: "Operation",  # Column C
            13: "Portfolio Name (Informational only)",  # Column N
            17: "State",  # Column R
            18: "Campaign State (Informational only)",  # Column S
            19: "Ad Group State (Informational only)",  # Column T
            27: "Bid",  # Column AB
            41: "Sales",  # Column AP
            37: "Impressions",  # Column AL
        }

        for col_idx, expected_name in required_column_checks.items():
            actual_name = df.columns[col_idx]
            if expected_name not in actual_name:
                self.warnings.append(
                    f"Column {col_idx + 1} should be '{expected_name}', found '{actual_name}'"
                )

        # Check for data issues
        if "Entity" in df.columns:
            entity_values = df["Entity"].value_counts()
            valid_entities = ["Keyword", "Product Targeting"]
            valid_count = sum(entity_values.get(e, 0) for e in valid_entities)

            if valid_count == 0:
                self.warnings.append(
                    "No rows with Entity = 'Keyword' or 'Product Targeting' found"
                )
            else:
                other_count = len(df) - valid_count
                if other_count > 0:
                    self.warnings.append(
                        f"{other_count} rows will be filtered out (Entity not Keyword/Product Targeting)"
                    )

        if "State" in df.columns:
            enabled_count = (df["State"] == "enabled").sum()
            if enabled_count == 0:
                self.warnings.append("No rows with State = 'enabled' found")
            else:
                disabled_count = len(df) - enabled_count
                if disabled_count > 0:
                    self.warnings.append(
                        f"{disabled_count} rows will be filtered out (State not enabled)"
                    )

        # Check Bid values
        if "Bid" in df.columns:
            bid_values = pd.to_numeric(df["Bid"], errors="coerce")
            high_bids = (bid_values > 1.25).sum()
            low_bids = (bid_values < 0.02).sum()

            if high_bids > 0:
                self.warnings.append(f"{high_bids} rows have Bid values above $1.25")
            if low_bids > 0:
                self.warnings.append(f"{low_bids} rows have Bid values below $0.02")

        return self._create_result(len(self.errors) == 0)

    def _create_result(self, is_valid: bool) -> Dict[str, Any]:
        """Create validation result dictionary"""
        return {
            "is_valid": is_valid,
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy(),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
        }

    def validate_file_size(self, file_size_bytes: int) -> bool:
        """Check if file size is within limits"""
        max_bytes = self.MAX_FILE_SIZE_MB * 1024 * 1024
        return file_size_bytes <= max_bytes
