"""
Application constants and configuration values
"""

# File limits
MAX_FILE_SIZE_MB = 40
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_ROWS = 500_000

# Bid ranges (for reporting only in mockup)
MIN_BID = 0.02
MAX_BID = 1.25

# Required columns for Bulk File
BULK_REQUIRED_COLUMNS = [
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

# Required columns for Template File
TEMPLATE_REQUIRED_COLUMNS = ["Portfolio Name", "Base Bid", "Target CPA"]

# Sheet names
SPONSORED_PRODUCTS_SHEET = "Sponsored Products Campaigns"

# Optimization types (mockup only has one)
OPTIMIZATION_TYPES = ["Zero Sales"]

# File naming patterns
OUTPUT_FILE_PREFIX = "Auto Optimized Bulk"
