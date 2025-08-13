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

    # Create tabs - Streamlit handles tab switching automatically
    tab1, tab2, tab3 = st.tabs([TAB_UPLOAD, TAB_VALIDATE, TAB_OUTPUT])

    # Render each tab content
    with tab1:
        upload_tab.render()

    with tab2:
        validate_tab.render()

    with tab3:
        output_tab.render()

    # Footer (optional)
    layout.add_vertical_space(3)
    layout.show_divider()
    st.caption("Bid Optimizer v1.0 (Mockup) - Internal Tool")


if __name__ == "__main__":
    main()
