import streamlit as st
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
panels_dir = os.path.dirname(current_dir)
ui_dir = os.path.dirname(panels_dir)
app_dir = os.path.dirname(ui_dir)
project_root = os.path.dirname(app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ui.components.alerts import (
    render_success_alert,
    render_error_alert,
    render_info_alert,
    render_warning_alert,
)
from ui.components.portfolio_list import render_portfolio_list
from business.services import Orchestrator


def render_validation_panel():
    """Render the validation panel"""

    # Only show if we have files uploaded
    if not st.session_state.get("template_file") or not st.session_state.get(
        "bulk_file"
    ):
        return

    # Don't show if we're processing or complete
    if st.session_state.get("current_state") in ["processing", "complete"]:
        return

    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Data Validation</h2>
    """,
        unsafe_allow_html=True,
    )

    # Get validation state
    validation_state = st.session_state.get("validation_state", "pending")

    if validation_state == "pending":
        # Show loading state and perform real validation
        with st.spinner("Validating..."):
            perform_real_validation()

    elif validation_state == "valid":
        # All portfolios valid
        render_valid_state()

    elif validation_state == "missing":
        # Missing portfolios found
        render_missing_state()

    elif validation_state == "ignored":
        # Some portfolios ignored
        render_ignored_state()

    elif validation_state == "error":
        # Validation errors
        render_error_state()

    # Close div
    st.markdown("</div>", unsafe_allow_html=True)


def perform_real_validation():
    """Perform real validation using Orchestrator"""

    try:
        # Get files from session state
        template_file = st.session_state.get("template_file")
        bulk_file = st.session_state.get("bulk_file")

        if not template_file or not bulk_file:
            st.session_state.validation_state = "error"
            st.session_state.validation_errors = ["Files not found in session"]
            st.rerun()
            return

        # Reset file pointers
        template_file.seek(0)
        bulk_file.seek(0)

        # Create orchestrator and validate
        orchestrator = Orchestrator()
        result = orchestrator.validate_files(template_file, bulk_file)

        # Store full result for debugging
        st.session_state.validation_result = result

        # Store DataFrames if available
        if "template_df" in result:
            st.session_state.template_df = result["template_df"]
        if "bulk_df" in result:
            st.session_state.bulk_df = result["bulk_df"]
        if "cleaned_bulk_df" in result:
            st.session_state.cleaned_bulk_df = result["cleaned_bulk_df"]

        # Process validation result
        if result["is_valid"]:
            if result.get("ignored_portfolios"):
                st.session_state.validation_state = "ignored"
                st.session_state.ignored_portfolios = result["ignored_portfolios"]
            else:
                st.session_state.validation_state = "valid"

            # Store statistics
            st.session_state.validation_stats = {
                "total_portfolios": result["stats"].get("template_portfolios", 0),
                "valid_rows": result["stats"].get("cleaned_rows", 0),
                "filtered_rows": result["stats"].get("filtered_rows", 0),
                "original_rows": result["stats"].get("original_rows", 0),
            }

        elif result.get("missing_portfolios"):
            st.session_state.validation_state = "missing"
            st.session_state.missing_portfolios = result["missing_portfolios"]

        else:
            st.session_state.validation_state = "error"
            st.session_state.validation_errors = result.get(
                "errors", ["Unknown validation error"]
            )

        # Store warnings but filter out the unwanted ones
        warnings = result.get("warnings", [])
        filtered_warnings = []
        for warning in warnings:
            # Skip warnings about Entity and State filtering
            if "Entity not Keyword/Product Targeting/Bidding Adjustment" in warning:
                continue
            if "State not enabled" in warning:
                continue
            filtered_warnings.append(warning)
        
        st.session_state.validation_warnings = filtered_warnings

    except Exception as e:
        st.session_state.validation_state = "error"
        st.session_state.validation_errors = [f"Validation failed: {str(e)}"]

    st.rerun()


def render_valid_state():
    """Render when all portfolios are valid"""

    # Success message
    render_success_alert(
        "All portfolios valid",
        "All portfolios in Bulk file have Base Bid values in Template",
    )

    # Show warnings if any (filtered)
    warnings = st.session_state.get("validation_warnings", [])
    if warnings:
        for warning in warnings[:3]:  # Show first 3 warnings
            render_warning_alert("", warning)
        if len(warnings) > 3:
            with st.expander(f"View all {len(warnings)} warnings"):
                for warning in warnings:
                    st.write(f"⚠️ {warning}")

    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Process Files",
            key="process_files_btn",
            type="primary",
            use_container_width=True,
            disabled=len(st.session_state.get("selected_optimizations", [])) == 0,
        ):
            # IMPORTANT: Set state to processing to trigger output panel
            st.session_state.current_state = "processing"
            st.rerun()

    # Show statistics if available
    if st.session_state.get("validation_stats"):
        stats = st.session_state.validation_stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Portfolios", stats.get("total_portfolios", 0))
        with col2:
            st.metric("Original Rows", f"{stats.get('original_rows', 0):,}")
        with col3:
            st.metric("After Cleaning", f"{stats.get('valid_rows', 0):,}")
        with col4:
            st.metric("Rows Filtered", f"{stats.get('filtered_rows', 0):,}")


def render_missing_state():
    """Render when portfolios are missing"""

    missing_portfolios = st.session_state.get("missing_portfolios", [])

    # Error message
    render_error_alert(
        "Missing portfolios found - Processing Blocked",
        f"The following portfolios are in Bulk but not in Template:",
    )

    # List of missing portfolios
    if missing_portfolios:
        render_portfolio_list(missing_portfolios, "Missing")

    # Info about blocking
    st.error(
        "You cannot proceed to processing until all portfolios are included in the Template."
    )

    # Upload new template button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Upload New Template",
            key="upload_new_template_btn",
            type="primary",
            use_container_width=True,
        ):
            # Reset template file
            st.session_state.template_file = None
            st.session_state.validation_state = "pending"
            st.rerun()

    # Info about next steps
    st.info(
        "Please add ALL the missing portfolios listed above to your Template file and upload again"
    )


def render_ignored_state():
    """Render when some portfolios are ignored"""

    ignored_portfolios = st.session_state.get("ignored_portfolios", [])
    ignored_count = len(ignored_portfolios)

    # Info message
    render_info_alert(
        f"Ignored portfolios: {ignored_count}",
        "These portfolios have Base Bid = 'Ignore' and will be skipped",
    )

    # Show ignored portfolios if any
    if ignored_portfolios:
        with st.expander("View Ignored Portfolios"):
            render_portfolio_list(ignored_portfolios, "Ignored")

    # Can still process
    render_valid_state()


def render_error_state():
    """Render when validation has errors"""

    errors = st.session_state.get("validation_errors", ["Unknown error"])

    # Show errors
    for error in errors:
        render_error_alert("Validation Error", error)

    # Upload new files button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Upload New Files",
            key="upload_new_files_btn",
            type="primary",
            use_container_width=True,
        ):
            # Reset both files
            st.session_state.template_file = None
            st.session_state.bulk_file = None
            st.session_state.validation_state = "pending"
            st.rerun()