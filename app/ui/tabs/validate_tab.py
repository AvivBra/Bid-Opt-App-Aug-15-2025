"""
Validate tab UI implementation - No emojis or icons
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from app.ui import widgets, messages, layout
from app.state.session import SessionManager
from config.ui_text import *
from config.settings import SessionKeys
from config.constants import TEMPLATE_REQUIRED_COLUMNS


def render():
    """Render the validate tab"""

    # Check if user can access this tab
    if not SessionManager.can_proceed_to_step(2):
        messages.show_error(
            "Please complete Step 1 (Upload) before proceeding to validation"
        )
        return

    # Tab header
    st.header(VALIDATE_HEADER)

    # File status summary
    st.subheader(VALIDATION_SUMMARY)
    template_file = SessionManager.get(SessionKeys.TEMPLATE_FILE)
    bulk_file = SessionManager.get(SessionKeys.BULK_FILE)
    widgets.show_file_status(template_file, bulk_file)

    layout.add_vertical_space(1)
    layout.show_divider()

    # Mock portfolio comparison (in real app, this would analyze files)
    # For mockup, we'll simulate different scenarios

    # Scenario selector (mockup only)
    with st.expander("Mockup Scenario Selector", expanded=True):
        scenario = st.radio(
            "Select validation scenario to demonstrate:",
            [
                "No Issues",
                "Missing Portfolios",
                "Excess Portfolios",
                "Both Missing and Excess",
            ],
            key="validation_scenario",
        )

    layout.add_vertical_space(1)

    # Process based on scenario
    if scenario == "No Issues":
        render_no_issues()
    elif scenario == "Missing Portfolios":
        render_missing_portfolios()
    elif scenario == "Excess Portfolios":
        render_excess_portfolios()
    else:  # Both Missing and Excess
        render_both_issues()


def render_no_issues():
    """Render UI when there are no portfolio issues"""
    messages.show_success("Portfolio validation complete - no issues found!")

    col1, col2 = st.columns(2)
    with col1:
        widgets.show_custom_metric("Missing Portfolios", "0")
    with col2:
        widgets.show_custom_metric("Excess Portfolios", "0")

    layout.add_vertical_space(2)

    # Continue button
    if widgets.action_button(CONTINUE_BUTTON, key="continue_to_output"):
        SessionManager.set(SessionKeys.CURRENT_STEP, 3)
        SessionManager.set(SessionKeys.VALIDATION_RESULTS, {"status": "complete"})
        SessionManager.set(SessionKeys.MISSING_PORTFOLIOS, [])
        st.rerun()


def render_missing_portfolios():
    """Render UI when there are missing portfolios"""
    # Mock missing portfolios
    missing = [
        "Portfolio_A",
        "Portfolio_B",
        "Portfolio_C",
        "Portfolio_D",
        "Portfolio_E",
    ]
    SessionManager.set(SessionKeys.MISSING_PORTFOLIOS, missing)

    messages.show_warning(
        f"Found {len(missing)} missing portfolios that need to be configured"
    )

    col1, col2 = st.columns(2)
    with col1:
        widgets.show_custom_metric("Missing Portfolios", len(missing))
    with col2:
        widgets.show_custom_metric("Excess Portfolios", "0")

    layout.add_vertical_space(1)

    # Download completion template
    st.subheader("Missing Portfolios - Action Required")
    st.write(
        "Download the completion template below, fill in the Base Bid values, and upload it back."
    )

    # Create completion template
    completion_df = pd.DataFrame(
        {
            "Portfolio Name": missing,
            "Base Bid": [""] * len(missing),
            "Target CPA": [""] * len(missing),
        }
    )

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        completion_df.to_excel(writer, index=False, sheet_name="Completion")
    buffer.seek(0)

    col1, col2 = st.columns(2)
    with col1:
        widgets.download_button(
            label=DOWNLOAD_COMPLETION_TEMPLATE,
            data=buffer,
            filename="completion_template.xlsx",
            key="download_completion",
        )

    with col2:
        # Upload completed template
        completed_file = widgets.file_uploader(
            label=UPLOAD_COMPLETION_TEMPLATE, key="upload_completion"
        )

        if completed_file:
            # Mock validation - clear missing portfolios
            SessionManager.set(SessionKeys.MISSING_PORTFOLIOS, [])
            messages.show_success(SUCCESS_MESSAGES["COMPLETION_UPLOADED"])
            st.rerun()


def render_excess_portfolios():
    """Render UI when there are excess portfolios"""
    # Mock excess portfolios
    excess = ["Portfolio_X", "Portfolio_Y", "Portfolio_Z"]
    SessionManager.set(SessionKeys.EXCESS_PORTFOLIOS, excess)

    messages.show_warning(f"Found {len(excess)} excess portfolios in template")

    col1, col2 = st.columns(2)
    with col1:
        widgets.show_custom_metric("Missing Portfolios", "0")
    with col2:
        widgets.show_custom_metric("Excess Portfolios", len(excess))

    layout.add_vertical_space(1)

    # Show excess list
    st.subheader("Excess Portfolios")
    st.write("These portfolios are in the template but not in the bulk file:")

    messages.show_portfolio_list(excess, "Excess Portfolios")

    # Copy button
    excess_text = "\n".join(excess)
    widgets.copy_to_clipboard_button(excess_text)

    layout.add_vertical_space(1)

    # Continue button (enabled for excess only)
    if widgets.action_button(CONTINUE_BUTTON, key="continue_with_excess"):
        SessionManager.set(SessionKeys.CURRENT_STEP, 3)
        SessionManager.set(SessionKeys.VALIDATION_RESULTS, {"status": "complete"})
        st.rerun()


def render_both_issues():
    """Render UI when there are both missing and excess portfolios"""
    # Mock portfolios
    missing = ["Portfolio_A", "Portfolio_B", "Portfolio_C"]
    excess = ["Portfolio_X", "Portfolio_Y"]
    SessionManager.set(SessionKeys.MISSING_PORTFOLIOS, missing)
    SessionManager.set(SessionKeys.EXCESS_PORTFOLIOS, excess)

    messages.show_warning(
        f"Found {len(missing)} missing and {len(excess)} excess portfolios"
    )

    col1, col2 = st.columns(2)
    with col1:
        widgets.show_custom_metric("Missing Portfolios", len(missing))
    with col2:
        widgets.show_custom_metric("Excess Portfolios", len(excess))

    layout.add_vertical_space(1)

    # Missing portfolios section
    st.subheader("1. Missing Portfolios - Action Required")
    st.write("Download and complete the template below:")

    # Create completion template
    completion_df = pd.DataFrame(
        {
            "Portfolio Name": missing,
            "Base Bid": [""] * len(missing),
            "Target CPA": [""] * len(missing),
        }
    )

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        completion_df.to_excel(writer, index=False, sheet_name="Completion")
    buffer.seek(0)

    col1, col2 = st.columns(2)
    with col1:
        widgets.download_button(
            label=DOWNLOAD_COMPLETION_TEMPLATE,
            data=buffer,
            filename="completion_template.xlsx",
            key="download_completion_both",
        )

    with col2:
        completed_file = widgets.file_uploader(
            label=UPLOAD_COMPLETION_TEMPLATE, key="upload_completion_both"
        )

        if completed_file:
            SessionManager.set(SessionKeys.MISSING_PORTFOLIOS, [])
            messages.show_success(SUCCESS_MESSAGES["COMPLETION_UPLOADED"])
            st.rerun()

    layout.add_vertical_space(1)
    layout.show_divider()

    # Excess portfolios section
    st.subheader("2. Excess Portfolios - For Information")
    messages.show_portfolio_list(excess, "Excess Portfolios")

    excess_text = "\n".join(excess)
    widgets.copy_to_clipboard_button(excess_text, key="copy_excess_both")

    layout.add_vertical_space(1)

    # Continue button (disabled until missing are resolved)
    missing_count = len(SessionManager.get(SessionKeys.MISSING_PORTFOLIOS, []))
    button_disabled = missing_count > 0

    if button_disabled:
        st.info("Resolve missing portfolios to enable the Continue button")

    if widgets.action_button(
        CONTINUE_BUTTON, key="continue_both", disabled=button_disabled
    ):
        SessionManager.set(SessionKeys.CURRENT_STEP, 3)
        SessionManager.set(SessionKeys.VALIDATION_RESULTS, {"status": "complete"})
        st.rerun()
