import streamlit as st
from ui.components.alerts import (
    render_success_alert,
    render_error_alert,
    render_info_alert,
)
from ui.components.portfolio_list import render_portfolio_list


def render_validation_panel():
    """Render the validation panel"""

    # Only show if we have files uploaded
    if not st.session_state.get("template_file") or not st.session_state.get(
        "bulk_file"
    ):
        return

    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Validation Results</h2>
    """,
        unsafe_allow_html=True,
    )

    # Get validation state
    validation_state = st.session_state.get("validation_state", "pending")

    if validation_state == "pending":
        # Show loading state
        with st.spinner("Validating..."):
            # In real implementation, this would trigger validation
            # For now, we'll simulate with mock data
            simulate_validation()

    elif validation_state == "valid":
        # All portfolios valid
        render_valid_state()

    elif validation_state == "missing":
        # Missing portfolios found
        render_missing_state()

    elif validation_state == "ignored":
        # Some portfolios ignored
        render_ignored_state()

    # Close div
    st.markdown("</div>", unsafe_allow_html=True)


def render_valid_state():
    """Render when all portfolios are valid"""

    # Success message
    render_success_alert(
        "All portfolios valid",
        "All portfolios in Bulk file have Base Bid values in Template",
    )

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
            st.session_state.current_state = "processing"
            st.rerun()

    # Show statistics if available
    if st.session_state.get("validation_stats"):
        stats = st.session_state.validation_stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Portfolios", stats.get("total_portfolios", 0))
        with col2:
            st.metric("Valid Rows", stats.get("valid_rows", 0))
        with col3:
            st.metric("Rows After Filtering", stats.get("filtered_rows", 0))


def render_missing_state():
    """Render when portfolios are missing"""

    missing_portfolios = st.session_state.get("missing_portfolios", [])

    # Error message
    render_error_alert(
        "Missing portfolios found",
        f"The following portfolios are in Bulk but not in Template:",
    )

    # List of missing portfolios
    if missing_portfolios:
        render_portfolio_list(missing_portfolios, "Missing Portfolios")

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
    st.info("Please add the missing portfolios to your Template file and upload again")


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


def simulate_validation():
    """Simulate validation for demo purposes"""
    import time

    time.sleep(1)  # Simulate processing time

    # Mock validation result
    # In real implementation, this would come from the orchestrator
    if "mock_scenario" in st.session_state:
        scenario = st.session_state.mock_scenario
        if scenario == "missing":
            st.session_state.validation_state = "missing"
            st.session_state.missing_portfolios = [
                "Portfolio_ABC",
                "Portfolio_DEF",
                "Portfolio_GHI",
            ]
        elif scenario == "ignored":
            st.session_state.validation_state = "ignored"
            st.session_state.ignored_portfolios = [
                "Portfolio_X",
                "Portfolio_Y",
                "Portfolio_Z",
            ]
        else:
            st.session_state.validation_state = "valid"
    else:
        # Default to valid
        st.session_state.validation_state = "valid"
        st.session_state.validation_stats = {
            "total_portfolios": 12,
            "valid_rows": 1234,
            "filtered_rows": 856,
        }

    st.rerun()
