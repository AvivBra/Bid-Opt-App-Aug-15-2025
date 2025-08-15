"""
Session state management for Bid Optimizer
"""

import streamlit as st
from typing import Any, Optional
from config.settings import SessionKeys, ProcessingStates


class SessionManager:
    """Manages session state for the application"""

    MAX_ITERATIONS = 10  # Maximum completion template iterations

    @classmethod
    def initialize(cls):
        """Initialize session state with default values"""
        # Current step tracking
        if SessionKeys.CURRENT_STEP not in st.session_state:
            st.session_state[SessionKeys.CURRENT_STEP] = 1

        # File storage
        if SessionKeys.BULK_FILE not in st.session_state:
            st.session_state[SessionKeys.BULK_FILE] = None

        if SessionKeys.TEMPLATE_FILE not in st.session_state:
            st.session_state[SessionKeys.TEMPLATE_FILE] = None

        # Selected optimizations
        if SessionKeys.SELECTED_OPTIMIZATIONS not in st.session_state:
            st.session_state[SessionKeys.SELECTED_OPTIMIZATIONS] = []

        # Validation results
        if SessionKeys.VALIDATION_RESULTS not in st.session_state:
            st.session_state[SessionKeys.VALIDATION_RESULTS] = {}

        # Virtual Map
        if SessionKeys.VIRTUAL_MAP not in st.session_state:
            st.session_state[SessionKeys.VIRTUAL_MAP] = {}

        # Processing state
        if SessionKeys.PROCESSING_STATE not in st.session_state:
            st.session_state[SessionKeys.PROCESSING_STATE] = ProcessingStates.IDLE

        # Messages
        if SessionKeys.ERROR_MESSAGES not in st.session_state:
            st.session_state[SessionKeys.ERROR_MESSAGES] = []

        if SessionKeys.SUCCESS_MESSAGES not in st.session_state:
            st.session_state[SessionKeys.SUCCESS_MESSAGES] = []

        if SessionKeys.WARNING_MESSAGES not in st.session_state:
            st.session_state[SessionKeys.WARNING_MESSAGES] = []

        # Completion template data
        if SessionKeys.COMPLETION_TEMPLATE not in st.session_state:
            st.session_state[SessionKeys.COMPLETION_TEMPLATE] = None

        # Missing and excess portfolios
        if SessionKeys.MISSING_PORTFOLIOS not in st.session_state:
            st.session_state[SessionKeys.MISSING_PORTFOLIOS] = []

        if SessionKeys.EXCESS_PORTFOLIOS not in st.session_state:
            st.session_state[SessionKeys.EXCESS_PORTFOLIOS] = []

        # Output files
        if SessionKeys.OUTPUT_FILES not in st.session_state:
            st.session_state[SessionKeys.OUTPUT_FILES] = {}

        # Iteration counter for Step 2
        if "completion_iteration_count" not in st.session_state:
            st.session_state["completion_iteration_count"] = 0

        # DataFrames for processing
        if "template_df" not in st.session_state:
            st.session_state["template_df"] = None

        if "bulk_df" not in st.session_state:
            st.session_state["bulk_df"] = None

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return st.session_state.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any):
        """Set value in session state"""
        st.session_state[key] = value

    @classmethod
    def clear(cls, key: str):
        """Clear specific key from session state"""
        if key in st.session_state:
            del st.session_state[key]

    @classmethod
    def reset_for_new_processing(cls):
        """Reset all session state for new processing"""
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        # Reinitialize
        cls.initialize()

        # Force rerun to start fresh
        st.rerun()

    @classmethod
    def can_proceed_to_step(cls, step: int) -> bool:
        """Check if user can proceed to specified step"""
        current_step = cls.get(SessionKeys.CURRENT_STEP, 1)

        if step == 1:
            return True  # Always can go to step 1

        elif step == 2:
            # Can proceed to step 2 if files uploaded and optimization selected
            has_template = cls.get(SessionKeys.TEMPLATE_FILE) is not None
            has_bulk = cls.get(SessionKeys.BULK_FILE) is not None
            has_optimization = len(cls.get(SessionKeys.SELECTED_OPTIMIZATIONS, [])) > 0

            return has_template and has_bulk and has_optimization

        elif step == 3:
            # Can proceed to step 3 if validation is complete
            validation_results = cls.get(SessionKeys.VALIDATION_RESULTS, {})
            return validation_results.get("status") == "complete"

        return False

    @classmethod
    def increment_iteration_count(cls) -> int:
        """Increment and return the iteration count"""
        count = st.session_state.get("completion_iteration_count", 0)
        count += 1
        st.session_state["completion_iteration_count"] = count
        return count

    @classmethod
    def get_iteration_count(cls) -> int:
        """Get current iteration count"""
        return st.session_state.get("completion_iteration_count", 0)

    @classmethod
    def check_iteration_limit(cls) -> bool:
        """Check if iteration limit has been reached"""
        return cls.get_iteration_count() >= cls.MAX_ITERATIONS

    @classmethod
    def reset_iteration_count(cls):
        """Reset iteration count to 0"""
        st.session_state["completion_iteration_count"] = 0

    @classmethod
    def add_error_message(cls, message: str):
        """Add error message to session"""
        errors = cls.get(SessionKeys.ERROR_MESSAGES, [])
        errors.append(message)
        cls.set(SessionKeys.ERROR_MESSAGES, errors)

    @classmethod
    def add_success_message(cls, message: str):
        """Add success message to session"""
        successes = cls.get(SessionKeys.SUCCESS_MESSAGES, [])
        successes.append(message)
        cls.set(SessionKeys.SUCCESS_MESSAGES, successes)

    @classmethod
    def add_warning_message(cls, message: str):
        """Add warning message to session"""
        warnings = cls.get(SessionKeys.WARNING_MESSAGES, [])
        warnings.append(message)
        cls.set(SessionKeys.WARNING_MESSAGES, warnings)

    @classmethod
    def clear_messages(cls):
        """Clear all messages"""
        cls.set(SessionKeys.ERROR_MESSAGES, [])
        cls.set(SessionKeys.SUCCESS_MESSAGES, [])
        cls.set(SessionKeys.WARNING_MESSAGES, [])
