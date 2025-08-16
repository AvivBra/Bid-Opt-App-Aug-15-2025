"""
UI Text Configuration
All user-facing text messages
"""

# Headers
HEADERS = {
    "MAIN": "Bid Optimizer - Bulk File",
    "UPLOAD": "Upload Files",
    "VALIDATION": "Validation Results",
    "OUTPUT": "Output Files",
    "OPTIMIZATIONS": "Select Optimizations",
}

# Button labels
BUTTONS = {
    "DOWNLOAD_TEMPLATE": "Download Template",
    "PROCESS_FILES": "Process Files",
    "UPLOAD_NEW_TEMPLATE": "Upload New Template",
    "DOWNLOAD_WORKING": "Download Working File",
    "DOWNLOAD_CLEAN": "Download Clean File",
    "RESET": "Reset",
    "LOAD_MOCK_DATA": "Load Mock Data",
}

# Success messages
SUCCESS_MESSAGES = {
    "FILES_UPLOADED": "Files uploaded successfully",
    "VALIDATION_COMPLETE": "All portfolios valid",
    "VALIDATION_DETAIL": "All portfolios in Bulk file have Base Bid values in Template",
    "PROCESSING_COMPLETE": "Processing complete",
    "FILES_READY": "Files ready for download",
    "RESET_COMPLETE": "Reset complete - ready for new files",
}

# Error messages
ERROR_MESSAGES = {
    "FILE_SIZE": "File exceeds 40MB limit",
    "FILE_FORMAT": "File must be Excel (.xlsx) or CSV format",
    "FILE_CORRUPT": "Cannot read file - it may be corrupted",
    "FILE_EMPTY": "File is empty - no data found",
    "SHEET_NOT_FOUND": "Required sheet 'Sponsored Products Campaigns' not found",
    "MISSING_COLUMNS": "Missing required columns: {columns}",
    "WRONG_COLUMN_ORDER": "Columns must be in exact order: Portfolio Name, Base Bid, Target CPA",
    "NO_DATA_ROWS": "Template has no data rows",
    "PORTFOLIO_EMPTY": "Portfolio Name cannot be empty in row {n}",
    "INVALID_BASE_BID": "Invalid Base Bid value in row {n} - must be number or 'Ignore'",
    "BASE_BID_RANGE": "Base Bid must be between 0.00 and 999.99",
    "DUPLICATE_PORTFOLIO": "Duplicate portfolio name: {name}",
    "ALL_IGNORED": "All portfolios marked as 'Ignore' - cannot proceed",
    "TOO_MANY_ROWS": "File contains more than 500,000 rows (found: {count})",
    "NO_VALID_ROWS": "No valid rows after filtering - check Entity and State columns",
    "MISSING_PORTFOLIOS": "Missing portfolios found",
    "MISSING_PORTFOLIOS_DETAIL": "The following portfolios are in Bulk but not in Template:",
}

# Warning messages
WARNING_MESSAGES = {
    "HIGH_BIDS": "{n} rows have Bid values above $1.25",
    "LOW_BIDS": "{n} rows have Bid values below $0.02",
    "IGNORED_PORTFOLIOS": 'Some portfolios marked as "Ignore" will be skipped',
    "SPECIAL_CHARS": "File contains special characters in portfolio names",
    "LARGE_FILE": "Large file detected - processing may take longer",
    "ROWS_SKIPPED": "{n} rows skipped due to missing data",
    "NO_OPTIMIZATION_SELECTED": "Please select at least one optimization to proceed",
}

# Info messages
INFO_MESSAGES = {
    "PROCESSING_ROWS": "Processing {n} rows...",
    "APPLYING_OPTIMIZATION": "Applying {optimization} optimization",
    "IGNORED_COUNT": "Ignored portfolios: {count}",
    "CLEANING_BULK": "Cleaning Bulk data (removing disabled items)",
    "GENERATING_FILES": "Generating output files...",
    "FILE_SIZE": "File size: {size} MB",
    "ROWS_AFTER_FILTER": "Rows after filtering: {count}",
    "OPTIMIZATIONS_SELECTED": "{count} optimization(s) selected",
    "TEMPLATE_NOT_UPLOADED": "Template: Not uploaded",
    "BULK_NOT_UPLOADED": "Bulk: Not uploaded",
    "TEMPLATE_UPLOADED": "Template: {name} ({size} KB)",
    "BULK_UPLOADED": "Bulk: {name} ({size} MB)",
}

# Pink notice messages
PINK_NOTICES = {
    "CALCULATION_ERRORS": "Please note: {n} calculation errors in {optimization} optimization",
    "CALCULATION_ERRORS_DETAIL": "These rows were skipped due to missing or invalid data.",
    "BID_ADJUSTMENTS": "Bid adjustments: {message}",
}

# Progress messages
PROGRESS_MESSAGES = {
    "UPLOADING": "Uploading... {percent}%",
    "VALIDATING": "Validating...",
    "COMPARING": "Comparing portfolios...",
    "PROCESSING": "Processing optimizations... {percent}%",
    "GENERATING_WORKING": "Generating Working file...",
    "GENERATING_CLEAN": "Generating Clean file...",
    "FINALIZING": "Finalizing...",
    "INITIALIZING": "Initializing optimizations...",
    "APPLYING_OPTIMIZATION": "Applying {optimization}...",
}

# File status
FILE_STATUS = {
    "NOT_UPLOADED": "✗ Not uploaded",
    "UPLOADED": "✓ {filename}",
    "HAS_ISSUES": "⚠️ Has issues",
}

# Tooltips/Help text
TOOLTIPS = {
    "DOWNLOAD_TEMPLATE": "Download an empty template with required columns",
    "UPLOAD_TEMPLATE": "Upload your filled template with portfolio Base Bids",
    "UPLOAD_BULK": "Upload your Amazon Bulk file (must contain 'Sponsored Products Campaigns' sheet)",
    "SELECT_OPTIMIZATIONS": "Choose which optimizations to apply to your data",
    "PROCESS_FILES": "Start processing with selected optimizations",
    "RESET": "Clear all data and start over",
}

# Section descriptions
DESCRIPTIONS = {
    "TEMPLATE_FILE": "Portfolio Name | Base Bid | Target CPA",
    "BULK_FILE": "Must contain 'Sponsored Products Campaigns' sheet",
    "FILES_GENERATED": "Files generated:",
    "WORKING_FILE_INFO": "• {size} MB\n• {sheets} sheets\n• {rows} rows",
    "CLEAN_FILE_INFO": "• {size} MB\n• {sheet} sheet\n• {rows} rows",
}

# Validation states descriptions
VALIDATION_STATES = {
    "PENDING": "Validation in progress...",
    "VALID": "All portfolios valid - ready to process",
    "MISSING": "Missing portfolios need to be added to template",
    "IGNORED": "Some portfolios will be ignored",
    "ERROR": "Validation failed - please check your files",
}

# Next steps instructions
NEXT_STEPS = {
    "AFTER_UPLOAD": "Files uploaded - validation will begin automatically",
    "AFTER_VALIDATION_SUCCESS": "Validation complete - click Process Files to continue",
    "AFTER_VALIDATION_FAIL": "Please add the missing portfolios to your Template file and upload again",
    "AFTER_PROCESSING": "Processing complete - download your optimized files",
    "AFTER_DOWNLOAD": "Files downloaded - click Reset to process new files",
}
