import pandas as pd
from io import BytesIO


class TemplateGenerator:
    """Generate empty template file"""

    def create_empty_template(self) -> bytes:
        """
        Create empty template file with required columns

        Returns:
            Excel file as bytes
        """
        # Create empty DataFrame with required columns
        df = pd.DataFrame(columns=["Portfolio Name", "Base Bid", "Target CPA"])

        # Create Excel file in memory
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Template", index=False)

            # Set column widths
            worksheet = writer.sheets["Template"]
            worksheet.column_dimensions["A"].width = 20  # Portfolio Name
            worksheet.column_dimensions["B"].width = 12  # Base Bid
            worksheet.column_dimensions["C"].width = 12  # Target CPA

        # Return file as bytes
        output.seek(0)
        return output.getvalue()

    def create_sample_template(self) -> bytes:
        """
        Create template file with sample data

        Returns:
            Excel file with examples
        """
        # Create DataFrame with sample data
        df = pd.DataFrame(
            {
                "Portfolio Name": [
                    "Example-Campaign-US",
                    "Example-Campaign-EU",
                    "Example-Campaign-UK",
                ],
                "Base Bid": [1.25, 0.95, "Ignore"],
                "Target CPA": [5.00, 4.50, None],
            }
        )

        # Create Excel file in memory
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Template", index=False)

            # Set column widths
            worksheet = writer.sheets["Template"]
            worksheet.column_dimensions["A"].width = 20
            worksheet.column_dimensions["B"].width = 12
            worksheet.column_dimensions["C"].width = 12

        output.seek(0)
        return output.getvalue()
