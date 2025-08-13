"""
UI text strings and messages - No emojis or icons
"""

# Application title and headers
TITLE = "Bid Optimizer - Bulk File"
TAB_UPLOAD = "Upload"
TAB_VALIDATE = "Validate"
TAB_OUTPUT = "Output"

# Step 1 - Upload
UPLOAD_HEADER = "Upload Files"
TEMPLATE_DOWNLOAD_BUTTON = "Download Template"
TEMPLATE_UPLOAD_LABEL = "Upload Template (xlsx/csv)"
BULK_UPLOAD_LABEL = "Upload Bulk (xlsx/csv, sheet: Sponsored Products Campaigns)"
OPTIMIZATION_HEADER = "Select Optimization Types"
OPTIMIZATION_ZERO_SALES = "Zero Sales"

# Step 2 - Validate
VALIDATE_HEADER = "Validate Portfolios"
VALIDATION_SUMMARY = "Validation Summary"
MISSING_PORTFOLIOS_LABEL = "Missing Portfolios"
EXCESS_PORTFOLIOS_LABEL = "Excess Portfolios"
DOWNLOAD_COMPLETION_TEMPLATE = "Download Completion Template"
UPLOAD_COMPLETION_TEMPLATE = "Upload Completed Template"
COPY_TO_CLIPBOARD = "Copy to Clipboard"
CONTINUE_BUTTON = "Continue"
BACK_BUTTON = "Back"

# Step 3 - Output
OUTPUT_HEADER = "Optimization & Output"
PROCESSING_MESSAGE = "Processing optimizations..."
DOWNLOAD_WORKING_FILE = "Download Working File"
DOWNLOAD_CLEAN_FILE = "Download Clean File"
NEW_PROCESSING_BUTTON = "New Processing"

# Error messages
ERROR_MESSAGES = {
    "S1-001": "File '{filename}' must be in Excel or CSV format",
    "S1-002": "File '{filename}' must not exceed 40MB",
    "S1-003": "File '{filename}' titles are incorrect",
    "S2-001": "Template format should only be Excel or CSV",
    "S2-002": "Template does not contain data",
    "S2-003": "Template titles are incorrect",
    "S2-004": "System cannot read template file",
    "S2-005": "All portfolios are marked as 'Ignore'. Cannot continue processing",
    "S2-006": "After first cleanse no rows are left in bulk file",
}

# Success messages
SUCCESS_MESSAGES = {
    "FILES_VALIDATED": "Files validated successfully",
    "TEMPLATE_UPLOADED": "Template uploaded successfully",
    "BULK_UPLOADED": "Bulk file uploaded successfully",
    "COMPLETION_UPLOADED": "Completion template uploaded successfully",
    "COPIED_TO_CLIPBOARD": "Copied to clipboard",
    "PROCESSING_COMPLETE": "Processing complete",
}

# Warning messages
WARNING_MESSAGES = {
    "MISSING_FOUND": "{count} missing portfolios found",
    "EXCESS_FOUND": "{count} excess portfolios found",
    "CALCULATION_ERRORS": "Please note: {count} calculation errors in {optimization_type}",
    "BIDS_OUT_OF_RANGE": "Bids outside range: {high_count} rows with bid >{max_bid}, {low_count} rows with bid <{min_bid}",
}

# Info messages
INFO_MESSAGES = {
    "NO_FILES": "Please upload both Template and Bulk files",
    "NO_OPTIMIZATION": "Please select at least one optimization type",
    "NO_MISSING": "No missing portfolios - ready to continue",
    "READY_TO_PROCESS": "Ready to process optimizations",
}
