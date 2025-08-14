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
from core.validate import bulk_cleanse, portfolios
from core.mapping.virtual_map import VirtualMap
from core.io import writers


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

    # Use centered content container
    with layout.create_content_container():
        st.subheader(VALIDATION_SUMMARY)

        # Get files from session
        template_file = SessionManager.get(SessionKeys.TEMPLATE_FILE)
        bulk_file = SessionManager.get(SessionKeys.BULK_FILE)
        template_df = st.session_state.get("template_df")
        bulk_df = st.session_state.get("bulk_df")

        # Show file status
        widgets.show_file_status(template_file, bulk_file)

        layout.add_vertical_space(1)

        # Initialize or get Virtual Map
        if "virtual_map" not in st.session_state:
            st.session_state["virtual_map"] = VirtualMap()
        elif not isinstance(st.session_state["virtual_map"], VirtualMap):
            # If it's a dict from old session, replace with VirtualMap
            st.session_state["virtual_map"] = VirtualMap()

        virtual_map = st.session_state["virtual_map"]

        # If this is first time in Step 2, initialize Virtual Map from template
        if len(virtual_map.data) == 0 and template_df is not None:
            initialize_virtual_map(virtual_map, template_df)

        # Perform initial cleanup and portfolio comparison
        if bulk_df is not None and template_df is not None:
            # Clean bulk data - remove ignored portfolios
            ignored_list = virtual_map.get_ignored()
            cleaned_bulk = bulk_cleanse.initial_cleanup(bulk_df, ignored_list)

            # Check if any rows left after cleanup
            if len(cleaned_bulk) == 0:
                messages.show_error(ERROR_MESSAGES["S2-006"])
                return

            # Get portfolios from CLEANED bulk for comparison
            cleaned_bulk_portfolios = bulk_cleanse.get_unique_portfolios(cleaned_bulk)

            # Get missing and excess portfolios - compare with CLEANED bulk
            missing = virtual_map.get_missing_portfolios(cleaned_bulk_portfolios)
            excess = virtual_map.get_excess_portfolios(cleaned_bulk_portfolios)

            # Store in session
            SessionManager.set(SessionKeys.MISSING_PORTFOLIOS, missing)
            SessionManager.set(SessionKeys.EXCESS_PORTFOLIOS, excess)

            st.subheader("Portfolio Comparison Results")

            # Handle different scenarios
            if len(missing) == 0 and len(excess) == 0:
                render_no_issues()
            elif len(missing) > 0 and len(excess) == 0:
                render_missing_portfolios(missing, virtual_map, cleaned_bulk_portfolios)
            elif len(missing) == 0 and len(excess) > 0:
                render_excess_portfolios(excess)
            else:
                render_both_issues(
                    missing, excess, virtual_map, cleaned_bulk_portfolios
                )


def initialize_virtual_map(virtual_map: VirtualMap, template_df: pd.DataFrame):
    """Initialize Virtual Map from template"""
    for _, row in template_df.iterrows():
        portfolio_name = row["Portfolio Name"]
        base_bid = row["Base Bid"]
        target_cpa = row.get("Target CPA", None)

        # Handle Ignore
        if str(base_bid).strip().lower() == "ignore":
            virtual_map.add_ignored(portfolio_name)
            continue

        try:
            base_bid_float = float(base_bid)
            target_cpa_float = (
                float(target_cpa) if target_cpa and str(target_cpa).strip() else None
            )
            virtual_map.add_portfolio(portfolio_name, base_bid_float, target_cpa_float)
        except (ValueError, TypeError):
            continue


def render_no_issues():
    """Render UI when there are no portfolio issues"""
    messages.show_success("Portfolio validation complete - no issues found!")

    widgets.show_custom_metric("Missing Portfolios", "0")
    widgets.show_custom_metric("Excess Portfolios", "0")

    layout.add_vertical_space(2)

    # Continue button
    if widgets.action_button(CONTINUE_BUTTON, key="continue_to_output"):
        # Freeze Virtual Map before going to Step 3
        st.session_state["virtual_map"].freeze()
        SessionManager.set(SessionKeys.CURRENT_STEP, 3)
        SessionManager.set(SessionKeys.VALIDATION_RESULTS, {"status": "complete"})
        st.rerun()


def render_missing_portfolios(
    missing: list, virtual_map: VirtualMap, bulk_portfolios: list
):
    """Render UI when there are missing portfolios"""
    messages.show_warning(
        f"Found {len(missing)} missing portfolios that need to be configured"
    )

    widgets.show_custom_metric("Missing Portfolios", len(missing))
    widgets.show_custom_metric("Excess Portfolios", "0")

    layout.add_vertical_space(1)

    # Download completion template
    st.subheader("Missing Portfolios - Action Required")
    st.write(
        "Download the completion template below, fill in the Base Bid values, and upload it back."
    )

    # Create completion template
    completion_buffer = writers.create_completion_template(missing)

    widgets.download_button(
        label=DOWNLOAD_COMPLETION_TEMPLATE,
        data=completion_buffer,
        filename="completion_template.xlsx",
        key="download_completion",
    )

    # Upload completed template
    completed_file = widgets.file_uploader(
        label=UPLOAD_COMPLETION_TEMPLATE, key="upload_completion"
    )

    if completed_file:
        # Read completion template
        completion_df = pd.read_excel(completed_file)

        # Merge into Virtual Map
        errors = virtual_map.merge_completion_template(completion_df, bulk_portfolios)

        if errors:
            for error in errors.values():
                messages.show_error(error)
        else:
            messages.show_success(SUCCESS_MESSAGES["COMPLETION_UPLOADED"])
            st.rerun()


def render_excess_portfolios(excess: list):
    """Render UI when there are excess portfolios"""
    messages.show_warning(f"Found {len(excess)} excess portfolios in template")

    widgets.show_custom_metric("Missing Portfolios", "0")
    widgets.show_custom_metric("Excess Portfolios", len(excess))

    layout.add_vertical_space(1)

    # Show excess list
    st.subheader("Excess Portfolios")
    st.write("These portfolios are in the template but not in the bulk file:")

    messages.show_portfolio_list(excess, "Excess Portfolios")

    # Copy button
    excess_text = "\n".join([str(p) for p in excess])
    widgets.copy_to_clipboard_button(excess_text)

    layout.add_vertical_space(1)

    # Continue button (enabled for excess only)
    if widgets.action_button(CONTINUE_BUTTON, key="continue_with_excess"):
        # Freeze Virtual Map before going to Step 3
        st.session_state["virtual_map"].freeze()
        SessionManager.set(SessionKeys.CURRENT_STEP, 3)
        SessionManager.set(SessionKeys.VALIDATION_RESULTS, {"status": "complete"})
        SessionManager.set(
            SessionKeys.PROCESSING_STATE, "idle"
        )  # Reset processing state
        st.rerun()


def render_both_issues(
    missing: list, excess: list, virtual_map: VirtualMap, bulk_portfolios: list
):
    """Render UI when there are both missing and excess portfolios"""
    messages.show_warning(
        f"Found {len(missing)} missing and {len(excess)} excess portfolios"
    )

    widgets.show_custom_metric("Missing Portfolios", len(missing))
    widgets.show_custom_metric("Excess Portfolios", len(excess))

    layout.add_vertical_space(1)

    # Missing portfolios section
    st.subheader("1. Missing Portfolios - Action Required")
    st.write("Download and complete the template below:")

    # Create completion template
    completion_buffer = writers.create_completion_template(missing)

    widgets.download_button(
        label=DOWNLOAD_COMPLETION_TEMPLATE,
        data=completion_buffer,
        filename="completion_template.xlsx",
        key="download_completion_both",
    )

    completed_file = widgets.file_uploader(
        label=UPLOAD_COMPLETION_TEMPLATE, key="upload_completion_both"
    )

    if completed_file:
        # Read completion template
        completion_df = pd.read_excel(completed_file)

        # Merge into Virtual Map
        errors = virtual_map.merge_completion_template(completion_df, bulk_portfolios)

        if errors:
            for error in errors.values():
                messages.show_error(error)
        else:
            messages.show_success(SUCCESS_MESSAGES["COMPLETION_UPLOADED"])
            st.rerun()

    layout.add_vertical_space(1)
    layout.show_divider()

    # Excess portfolios section
    st.subheader("2. Excess Portfolios - For Information")
    messages.show_portfolio_list(excess, "Excess Portfolios")

    excess_text = "\n".join([str(p) for p in excess])
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
        # Freeze Virtual Map before going to Step 3
        st.session_state["virtual_map"].freeze()
        SessionManager.set(SessionKeys.CURRENT_STEP, 3)
        SessionManager.set(SessionKeys.VALIDATION_RESULTS, {"status": "complete"})
        st.rerun()
