"""
Application settings and configuration
"""

# App settings
APP_NAME = "Bid Optimizer - Bulk"
APP_VERSION = "1.0.0 (Mockup)"

# Debug settings
DEBUG_MODE = False
USE_MOCK_DATA = False


# Session state keys
class SessionKeys:
    """Session state keys for consistency"""

    CURRENT_STEP = "current_step"
    BULK_FILE = "bulk_file"
    TEMPLATE_FILE = "template_file"
    SELECTED_OPTIMIZATIONS = "selected_optimizations"
    VALIDATION_RESULTS = "validation_results"
    VIRTUAL_MAP = "virtual_map"
    PROCESSING_STATE = "processing_state"
    ERROR_MESSAGES = "error_messages"
    SUCCESS_MESSAGES = "success_messages"
    WARNING_MESSAGES = "warning_messages"
    COMPLETION_TEMPLATE = "completion_template"
    MISSING_PORTFOLIOS = "missing_portfolios"
    EXCESS_PORTFOLIOS = "excess_portfolios"
    OUTPUT_FILES = "output_files"


# Processing states
class ProcessingStates:
    """Processing state constants"""

    IDLE = "idle"
    UPLOADING = "uploading"
    VALIDATING = "validating"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


# File types
class FileTypes:
    """File type constants"""

    EXCEL = "xlsx"
    CSV = "csv"


# Completion loop protection
MAX_COMPLETION_LOOPS = 10
