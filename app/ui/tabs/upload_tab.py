"""
Upload tab UI implementation - No emojis or icons
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from app.ui import widgets, messages, layout
from app.state.session import SessionManager
from config.ui_text import *
from config.settings import SessionKeys
from config.constants import (
    BULK_REQUIRED_COLUMNS,
    TEMPLATE_REQUIRED_COLUMNS,
    SPONSORED_PRODUCTS_SHEET,
    MAX_FILE_SIZE_MB,
)
from core.io import readers


def render():
    """Render the upload tab"""

    # Tab header
    st.header(UPLOAD_HEADER)

    # Create two columns directly without container
    col1, col2 = st.columns(2)

    with col1:
        render_files_section()

    with col2:
        render_optimization_section()

    # Check if can proceed
    check_and_enable_continue()


def render_files_section():
    """Render the files upload section"""
    layout.show_subheader("Files")

    # Download template button
    template_buffer = widgets.create_empty_template()
    widgets.download_button(
        label=TEMPLATE_DOWNLOAD_BUTTON,
        data=template_buffer,
        filename="template.xlsx",
        key="download_template",
    )

    layout.add_vertical_space(1)

    # Upload Template
    template_file = widgets.file_uploader(
        label=TEMPLATE_UPLOAD_LABEL,
        key="template_upload",
        help_text="Upload the completed template file",
    )

    if template_file:
        process_template_file(template_file)

    layout.add_vertical_space(1)

    # Upload Bulk
    bulk_file = widgets.file_uploader(
        label=BULK_UPLOAD_LABEL,
        key="bulk_upload",
        help_text="Upload your Amazon Bulk file",
    )

    if bulk_file:
        process_bulk_file(bulk_file)


def render_optimization_section():
    """Render optimization selection section"""
    layout.show_subheader("Select Optimization Types")

    # For mockup, only Zero Sales
    selected_optimizations = []

    if st.checkbox(OPTIMIZATION_ZERO_SALES, value=True, key="opt_zero_sales"):
        selected_optimizations.append("Zero Sales")

    # Store selections
    SessionManager.set(SessionKeys.SELECTED_OPTIMIZATIONS, selected_optimizations)

    # Show future optimizations (disabled)
    with st.expander("Future Optimization Types (Coming Soon)", expanded=False):
        st.caption("• Portfolio Bid Optimization")
        st.caption("• Budget Optimization")
        st.caption("• Keyword Optimization")
        st.caption("• Product Targeting Optimization")
        st.caption("• Day Parting Optimization")
        st.caption("• Placement Optimization")
        st.caption("• Search Term Optimization")
        st.caption("• Negative Keyword Optimization")
        st.caption("• ASIN Targeting Optimization")
        st.caption("• Category Targeting Optimization")
        st.caption("• Budget Allocation Optimization")
        st.caption("• Campaign Structure Optimization")
        st.caption("• Bid Modifier Optimization")

    # Show validation status
    layout.add_vertical_space(2)
    show_validation_status()


def process_template_file(file: BytesIO):
    """Process uploaded template file"""
    try:
        # Check file size
        if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            messages.show_error(ERROR_MESSAGES["S1-002"].format(filename=file.name))
            return

        # Read file
        try:
            df = pd.read_excel(file)
            st.session_state["template_df"] = df
        except:
            file.seek(0)
            df = pd.read_csv(file)
            st.session_state["template_df"] = df

        # Validate headers
        if list(df.columns) != TEMPLATE_REQUIRED_COLUMNS:
            messages.show_error(ERROR_MESSAGES["S1-003"].format(filename=file.name))
            SessionManager.clear(SessionKeys.TEMPLATE_FILE)
            return

        # Check if empty
        if len(df) == 0:
            messages.show_error("Template file is empty. Please add portfolio data.")
            SessionManager.clear(SessionKeys.TEMPLATE_FILE)
            return

        # Store in session
        SessionManager.set(SessionKeys.TEMPLATE_FILE, file)
        messages.show_success(SUCCESS_MESSAGES["TEMPLATE_UPLOADED"])

    except Exception as e:
        messages.show_error(f"Error processing template file: {str(e)}")
        SessionManager.clear(SessionKeys.TEMPLATE_FILE)


def process_bulk_file(file: BytesIO):
    """Process uploaded bulk file"""
    try:
        # Check file size
        if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            messages.show_error(ERROR_MESSAGES["S1-002"].format(filename=file.name))
            return

        # Try to read as Excel first
        try:
            # Check for required sheet
            excel_file = pd.ExcelFile(file, engine="openpyxl")
            if SPONSORED_PRODUCTS_SHEET not in excel_file.sheet_names:
                messages.show_error(
                    f"Sheet '{SPONSORED_PRODUCTS_SHEET}' not found in bulk file"
                )
                SessionManager.clear(SessionKeys.BULK_FILE)
                return

            # Read the specific sheet
            df = pd.read_excel(
                file, sheet_name=SPONSORED_PRODUCTS_SHEET, engine="openpyxl"
            )
            st.session_state["bulk_df"] = df

        except:
            # Try as CSV
            file.seek(0)
            df = pd.read_csv(file)
            st.session_state["bulk_df"] = df

        # Validate headers
        if list(df.columns) != BULK_REQUIRED_COLUMNS:
            messages.show_error(ERROR_MESSAGES["S1-003"].format(filename=file.name))
            SessionManager.clear(SessionKeys.BULK_FILE)
            return

        # Store in session
        SessionManager.set(SessionKeys.BULK_FILE, file)
        messages.show_success(SUCCESS_MESSAGES["BULK_UPLOADED"])

    except Exception as e:
        messages.show_error(f"Error processing bulk file: {str(e)}")
        SessionManager.clear(SessionKeys.BULK_FILE)


def show_validation_status():
    """Show current validation status"""
    template_file = SessionManager.get(SessionKeys.TEMPLATE_FILE)
    bulk_file = SessionManager.get(SessionKeys.BULK_FILE)
    optimizations = SessionManager.get(SessionKeys.SELECTED_OPTIMIZATIONS, [])

    if template_file and bulk_file and optimizations:
        messages.show_success(SUCCESS_MESSAGES["FILES_VALIDATED"])
    else:
        missing = []
        if not template_file:
            missing.append("Template file")
        if not bulk_file:
            missing.append("Bulk file")
        if not optimizations:
            missing.append("Optimization selection")

        if missing:
            messages.show_info(f"Waiting for: {', '.join(missing)}")


def check_and_enable_continue():
    """Check if all requirements are met and show continue button"""
    template_file = SessionManager.get(SessionKeys.TEMPLATE_FILE)
    bulk_file = SessionManager.get(SessionKeys.BULK_FILE)
    optimizations = SessionManager.get(SessionKeys.SELECTED_OPTIMIZATIONS, [])

    if template_file and bulk_file and optimizations:
        layout.add_vertical_space(2)
        layout.show_divider()

        # Continue button
        if widgets.action_button("Continue to Validation", key="continue_to_validate"):
            SessionManager.set(SessionKeys.CURRENT_STEP, 2)
            st.session_state["switch_to_validate"] = True
            st.rerun()
