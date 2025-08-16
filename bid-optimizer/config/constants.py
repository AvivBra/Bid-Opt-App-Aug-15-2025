"""
Application Constants
All constant values used throughout the application
"""

# File size limits
MAX_FILE_SIZE_MB = 40
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_ROWS = 500000

# Column requirements
TEMPLATE_COLUMNS = ["Portfolio Name", "Base Bid", "Target CPA"]
TEMPLATE_COLUMNS_COUNT = 3

BULK_COLUMNS_COUNT = 46
BULK_REQUIRED_SHEET = "Sponsored Products Campaigns"

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

# Filtering criteria
VALID_ENTITIES = ["Keyword", "Product Targeting"]
ENABLED_STATE = "enabled"

# Bid limits
MIN_BID = 0.02
MAX_BID = 1.25
DEFAULT_BID = 0.02

# Optimization names
OPTIMIZATIONS = [
    "Zero Sales",
    "Portfolio Bid Optimization",
    "Budget Optimization",
    "Keyword Optimization",
    "ASIN Targeting",
    "Negative Keyword Optimization",
    "Placement Optimization",
    "Dayparting Optimization",
    "Search Term Optimization",
    "Product Targeting Optimization",
    "Campaign Structure Optimization",
    "Bid Adjustment Optimization",
    "Match Type Optimization",
    "Geographic Optimization",
]

DEFAULT_OPTIMIZATION = "Zero Sales"

# Application states
STATES = {
    "UPLOAD": "upload",
    "VALIDATE": "validate",
    "READY": "ready",
    "PROCESSING": "processing",
    "COMPLETE": "complete",
}

# File types
FILE_TYPES = {
    "TEMPLATE": "template",
    "BULK": "bulk",
    "WORKING": "Working",
    "CLEAN": "Clean",
}

# Colors (for consistency)
COLORS = {
    "PRIMARY": "#FF0000",
    "SUCCESS": "#28a745",
    "ERROR": "#dc3545",
    "WARNING": "#ffc107",
    "INFO": "#17a2b8",
    "PINK": "#FFE4E1",
    "WHITE": "#FFFFFF",
    "BLACK": "#000000",
    "GRAY": "#6c757d",
}

# Time formats
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H-%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Processing timeouts (seconds)
UPLOAD_TIMEOUT = 30
VALIDATION_TIMEOUT = 10
PROCESSING_TIMEOUT = 120
OUTPUT_TIMEOUT = 60

# Debug mode
DEBUG_MODE = True  # Set to True to enable mock data buttons
