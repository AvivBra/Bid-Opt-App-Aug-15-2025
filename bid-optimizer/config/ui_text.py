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