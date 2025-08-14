"""
Main application entry point for Bid Optimizer
Run with: streamlit run app/main.py
"""

import sys
import os

# Add parent directory to Python path to fix imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import streamlit as st

# Now import our modules
from app.ui import layout
from app.ui.tabs import upload_tab, validate_tab, output_tab
from app.state.session import SessionManager
from config.ui_text import TAB_UPLOAD, TAB_VALIDATE, TAB_OUTPUT


def main():
    """Main application function"""

    # Setup page configuration
    layout.setup_page()

    # Initialize session state
    SessionManager.initialize()

    # Show header
    layout.show_header()

    # Check if we need to switch tabs
    if st.session_state.get("switch_to_validate"):
        st.session_state["switch_to_validate"] = False
        default_tab = 1  # Validate tab
    elif st.session_state.get("switch_to_output"):
        st.session_state["switch_to_output"] = False
        default_tab = 2  # Output tab
    else:
        # Check current step to determine default tab
        current_step = st.session_state.get("current_step", 1)
        if current_step >= 3:
            default_tab = 2  # Output tab
        elif current_step >= 2:
            default_tab = 1  # Validate tab
        else:
            default_tab = 0  # Upload tab

    # Create tabs with default selection
    tabs = st.tabs([TAB_UPLOAD, TAB_VALIDATE, TAB_OUTPUT])

    # Render each tab content
    with tabs[0]:
        upload_tab.render()

    with tabs[1]:
        validate_tab.render()

    with tabs[2]:
        output_tab.render()

    # Footer (optional)
    layout.add_vertical_space(3)
    layout.show_divider()
    st.caption("Bid Optimizer v1.0 (Mockup) - Internal Tool")


if __name__ == "__main__":
    main()
