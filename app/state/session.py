"""
Session state management for the application
"""

import streamlit as st
from typing import Any, Optional, Dict, List
from config.settings import SessionKeys, ProcessingStates


class SessionManager:
    """Manages Streamlit session state"""

    @staticmethod
    def initialize():
        """Initialize session state with default values"""
        defaults = {
            SessionKeys.CURRENT_STEP: 1,
            SessionKeys.BULK_FILE: None,
            SessionKeys.TEMPLATE_FILE: None,
            SessionKeys.SELECTED_OPTIMIZATIONS: [],
            SessionKeys.VALIDATION_RESULTS: None,
            SessionKeys.VIRTUAL_MAP: {},
            SessionKeys.PROCESSING_STATE: ProcessingStates.IDLE,
            SessionKeys.ERROR_MESSAGES: [],
            SessionKeys.SUCCESS_MESSAGES: [],
            SessionKeys.WARNING_MESSAGES: [],
            SessionKeys.COMPLETION_TEMPLATE: None,
            SessionKeys.MISSING_PORTFOLIOS: [],
            SessionKeys.EXCESS_PORTFOLIOS: [],
            SessionKeys.OUTPUT_FILES: {},
        }

        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any):
        """Set value in session state"""
        st.session_state[key] = value

    @staticmethod
    def clear():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        SessionManager.initialize()

    @staticmethod
    def reset_for_new_processing():
        """Reset state for new processing"""
        SessionManager.clear()
        st.rerun()

    @staticmethod
    def can_proceed_to_step(step: int) -> bool:
        """Check if user can proceed to given step"""
        if step == 1:
            return True

        elif step == 2:
            # Can proceed to step 2 if files are uploaded and optimization selected
            # Check in st.session_state directly
            has_bulk = st.session_state.get(SessionKeys.BULK_FILE) is not None
            has_template = st.session_state.get(SessionKeys.TEMPLATE_FILE) is not None
            has_optimization = (
                len(st.session_state.get(SessionKeys.SELECTED_OPTIMIZATIONS, [])) > 0
            )
            return has_bulk and has_template and has_optimization

        elif step == 3:
            # Can proceed to step 3 if validation is complete
            # For mockup, just check if step 2 requirements are met
            can_do_step2 = SessionManager.can_proceed_to_step(2)
            # In real app would check validation_results, for now just check step 2
            return can_do_step2

        return False

    @staticmethod
    def add_error(message: str):
        """Add error message"""
        errors = SessionManager.get(SessionKeys.ERROR_MESSAGES, [])
        if message not in errors:
            errors.append(message)
            SessionManager.set(SessionKeys.ERROR_MESSAGES, errors)

    @staticmethod
    def add_success(message: str):
        """Add success message"""
        successes = SessionManager.get(SessionKeys.SUCCESS_MESSAGES, [])
        if message not in successes:
            successes.append(message)
            SessionManager.set(SessionKeys.SUCCESS_MESSAGES, successes)

    @staticmethod
    def add_warning(message: str):
        """Add warning message"""
        warnings = SessionManager.get(SessionKeys.WARNING_MESSAGES, [])
        if message not in warnings:
            warnings.append(message)
            SessionManager.set(SessionKeys.WARNING_MESSAGES, warnings)

    @staticmethod
    def clear_messages():
        """Clear all messages"""
        SessionManager.set(SessionKeys.ERROR_MESSAGES, [])
        SessionManager.set(SessionKeys.SUCCESS_MESSAGES, [])
        SessionManager.set(SessionKeys.WARNING_MESSAGES, [])
