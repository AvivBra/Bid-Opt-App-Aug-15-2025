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
        # Validation error
        render_error_state()

    st.markdown("</div>", unsafe_allow_html=True)


def perform_real_validation():
    """Perform real validation using Orchestrator"""

    try:
        # Get files from session state
        template_file = st.session_state.get("template_file")
        bulk_file = st.session_state.get("bulk_file")

        print(f"DEBUG: Template file type: {type(template_file)}")
        print(f"DEBUG: Bulk file type: {type(bulk_file)}")

        # Reset file positions if needed
        if hasattr(template_file, "seek"):
            template_file.seek(0)
        if hasattr(bulk_file, "seek"):
            bulk_file.seek(0)

        # Create orchestrator and validate
        orchestrator = Orchestrator()
        result = orchestrator.validate_files(template_file, bulk_file)

        print(f"DEBUG: Validation result: {result.get('is_valid')}")
        print(f"DEBUG: Errors: {result.get('errors')}")
        print(f"DEBUG: Missing portfolios: {result.get('missing_portfolios')}")

        # Store the result in session state
        st.session_state["validation_result"] = result

        # Store separated dataframes and template for later processing
        if result.get("separated_dataframes"):
            st.session_state["separated_dataframes"] = result["separated_dataframes"]
        if result.get("template_df") is not None:
            st.session_state["template_df"] = result["template_df"]

        # Determine validation state
        if not result["is_valid"]:
            if result.get("errors"):
                st.session_state["validation_state"] = "error"
                st.session_state["validation_errors"] = result["errors"]
            elif result.get("missing_portfolios"):
                st.session_state["validation_state"] = "missing"
                st.session_state["missing_portfolios"] = result["missing_portfolios"]
        elif result.get("ignored_portfolios"):
            st.session_state["validation_state"] = "ignored"
            st.session_state["ignored_portfolios"] = result["ignored_portfolios"]
        else:
            st.session_state["validation_state"] = "valid"

        # Store stats
        if result.get("stats"):
            st.session_state["validation_stats"] = result["stats"]

    except Exception as e:
        print(f"ERROR in validation: {e}")
        import traceback

        traceback.print_exc()

        st.session_state["validation_state"] = "error"
        st.session_state["validation_errors"] = [f"Validation failed: {str(e)}"]

    # Force rerun to show the results
    st.rerun()


def render_valid_state():
    """Render when all portfolios are valid"""

    # Success message
    render_success_alert(
        "All portfolios valid", "All portfolios in Bulk exist in Template"
    )

    # Show stats if available
    stats = st.session_state.get("validation_stats", {})
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Template Rows", stats.get("template_rows", 0))
        with col2:
            st.metric("Targets Rows", stats.get("targets_rows", 0))
        with col3:
            st.metric("Total Bulk Rows", stats.get("bulk_rows", 0))

    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "Process Files",
            key="process_files_btn",
            type="primary",
            use_container_width=True,
        ):
            # Move to processing state
            st.session_state.current_state = "processing"
            st.rerun()


def render_missing_state():
    """Render when missing portfolios are found"""

    missing_portfolios = st.session_state.get("missing_portfolios", [])

    # Error message
    render_error_alert(
        "Missing portfolios found - Processing Blocked",
        f"The following {len(missing_portfolios)} portfolios are in Bulk but not in Template",
    )

    # Show missing portfolios
    if missing_portfolios:
        render_portfolio_list(missing_portfolios, "Missing")

    # Warning message
    st.warning(
        "You must add ALL these portfolios to your Template file to continue",
        icon="⚠️",
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
