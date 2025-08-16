"""
Session State Manager
Manages all application state and transitions
"""

import streamlit as st
from typing import Any, Dict, List, Optional


class SessionStateManager:
    """Manages application state and transitions"""

    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        defaults = {
            "current_state": "upload",
            "template_file": None,
            "bulk_file": None,
            "template_df": None,
            "bulk_df": None,
            "cleaned_bulk_df": None,
            "selected_optimizations": ["Zero Sales"],
            "validation_state": "pending",
            "validation_result": None,
            "missing_portfolios": [],
            "ignored_portfolios": [],
            "excess_portfolios": [],
            "validation_stats": {},
            "output_files": {},
            "processing_stats": {},
            "mock_scenario": "valid",  # For testing
            "use_mock_data": False,  # Flag for mock data
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def set(key: str, value: Any):
        """Set a value in session state"""
        st.session_state[key] = value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a value from session state"""
        return st.session_state.get(key, default)

    @staticmethod
    def clear():
        """Clear all session state except defaults"""
        # Keep only essential keys
        keep_keys = ["current_state"]
        for key in list(st.session_state.keys()):
            if key not in keep_keys:
                del st.session_state[key]

        # Reinitialize
        SessionStateManager.initialize()

    @staticmethod
    def get_current_state() -> str:
        """Get current application state"""
        return st.session_state.get("current_state", "upload")

    @staticmethod
    def set_current_state(state: str):
        """Set current application state"""
        valid_states = ["upload", "validate", "ready", "processing", "complete"]
        if state in valid_states:
            st.session_state.current_state = state

    @staticmethod
    def can_proceed() -> bool:
        """Check if can proceed to next step"""
        state = SessionStateManager.get_current_state()

        if state == "upload":
            # Can proceed if both files uploaded
            return bool(
                st.session_state.get("template_file")
                and st.session_state.get("bulk_file")
            )

        elif state == "validate":
            # Can proceed if validation passed
            validation = st.session_state.get("validation_result", {})
            return validation.get("is_valid", False) if validation else False

        elif state == "ready":
            # Can proceed if optimizations selected
            return len(st.session_state.get("selected_optimizations", [])) > 0

        return False

    @staticmethod
    def transition_to_next_state():
        """Transition to next state in flow"""
        current = SessionStateManager.get_current_state()

        transitions = {
            "upload": "validate",
            "validate": "ready",
            "ready": "processing",
            "processing": "complete",
            "complete": "upload",  # Reset
        }

        if current in transitions:
            next_state = transitions[current]
            SessionStateManager.set_current_state(next_state)

            # Handle special transitions
            if next_state == "validate":
                st.session_state.validation_state = "pending"
            elif next_state == "upload":
                SessionStateManager.clear()

    @staticmethod
    def update_validation_result(
        is_valid: bool,
        missing: List[str] = None,
        ignored: List[str] = None,
        messages: List[str] = None,
    ):
        """Update validation result"""
        st.session_state.validation_result = {
            "is_valid": is_valid,
            "missing_portfolios": missing or [],
            "ignored_portfolios": ignored or [],
            "messages": messages or [],
        }

        # Update related states
        st.session_state.missing_portfolios = missing or []
        st.session_state.ignored_portfolios = ignored or []

        # Set validation state
        if is_valid:
            st.session_state.validation_state = "valid"
        elif missing:
            st.session_state.validation_state = "missing"
        elif ignored:
            st.session_state.validation_state = "ignored"

    @staticmethod
    def update_processing_stats(stats: Dict[str, Any]):
        """Update processing statistics"""
        st.session_state.processing_stats = stats

    @staticmethod
    def update_output_files(
        working_file: bytes = None,
        clean_file: bytes = None,
        working_filename: str = None,
        clean_filename: str = None,
    ):
        """Update output files"""
        if working_file:
            st.session_state.output_files["working"] = working_file
            st.session_state.output_files["working_filename"] = working_filename

        if clean_file:
            st.session_state.output_files["clean"] = clean_file
            st.session_state.output_files["clean_filename"] = clean_filename

    @staticmethod
    def is_ready_to_process() -> bool:
        """Check if ready to process"""
        return (
            st.session_state.get("template_file") is not None
            and st.session_state.get("bulk_file") is not None
            and st.session_state.get("validation_result", {}).get("is_valid", False)
            and len(st.session_state.get("selected_optimizations", [])) > 0
        )

    @staticmethod
    def get_state_summary() -> Dict[str, Any]:
        """Get summary of current state"""
        validation_result = st.session_state.get("validation_result")
        is_validated = False
        if validation_result and isinstance(validation_result, dict):
            is_validated = validation_result.get("is_valid", False)

        return {
            "current_state": SessionStateManager.get_current_state(),
            "has_template": st.session_state.get("template_file") is not None,
            "has_bulk": st.session_state.get("bulk_file") is not None,
            "is_validated": is_validated,
            "optimizations_count": len(
                st.session_state.get("selected_optimizations", [])
            ),
            "can_proceed": SessionStateManager.can_proceed(),
        }
