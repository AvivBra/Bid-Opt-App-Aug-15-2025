import streamlit as st
import sys
import os

# Add app directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(app_dir)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ui.layout import apply_custom_css, create_header
from ui.panels.upload_panel import render_upload_panel
from ui.panels.validate_panel import render_validation_panel
from ui.panels.output_panel import render_output_panel
from state.session import SessionStateManager
from state.mock_data import MockDataProvider
from config.constants import DEBUG_MODE
from config.ui_text import BUTTONS


def render_page():
    """Main page renderer with state management"""

    # Initialize session state
    SessionStateManager.initialize()

    # Apply styling
    apply_custom_css()

    # Header
    create_header()

    # Debug controls (only in debug mode)
    if DEBUG_MODE:
        render_debug_controls()

    # Panels based on current state
    render_panels_based_on_state()


def render_panels_based_on_state():
    """Render panels based on current application state"""

    current_state = SessionStateManager.get_current_state()

    # Always show upload panel
    render_upload_panel()

    # Show validation panel if files uploaded
    if SessionStateManager.get("template_file") and SessionStateManager.get(
        "bulk_file"
    ):
        # Trigger validation automatically
        if SessionStateManager.get("validation_state") == "pending":
            trigger_mock_validation()

        render_validation_panel()

    # Show output panel if in processing or complete state
    if current_state in ["processing", "complete"]:
        render_output_panel()


def trigger_mock_validation():
    """Trigger mock validation based on selected scenario"""

    # Get mock scenario
    scenario = SessionStateManager.get("mock_scenario", "valid")

    # Get validation result from mock data
    scenarios = MockDataProvider.get_validation_scenarios()
    result = scenarios.get(scenario, scenarios["valid"])

    # Update session state
    SessionStateManager.update_validation_result(
        is_valid=result["is_valid"],
        missing=result.get("missing_portfolios"),
        ignored=result.get("ignored_portfolios"),
        messages=result.get("messages"),
    )

    # Update validation stats
    SessionStateManager.set("validation_stats", result.get("stats", {}))

    # Update validation state
    if result["is_valid"]:
        if result.get("ignored_portfolios"):
            SessionStateManager.set("validation_state", "ignored")
        else:
            SessionStateManager.set("validation_state", "valid")
    else:
        SessionStateManager.set("validation_state", "missing")

    # If valid, transition to ready state
    if result["is_valid"]:
        SessionStateManager.set_current_state("ready")


def render_debug_controls():
    """Render debug controls for testing different scenarios"""

    with st.expander("🔧 Debug Controls (Dev Only)"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Load Mock Data**")

            # Scenario selector
            scenario = st.selectbox(
                "Select Scenario",
                options=["valid", "missing", "ignored", "mixed"],
                key="mock_scenario_selector",
                help="Choose a test scenario",
            )

            # Load mock data button
            if st.button(BUTTONS["LOAD_MOCK_DATA"], key="load_mock_btn"):
                load_mock_data(scenario)

        with col2:
            st.markdown("**Current State**")
            state_info = SessionStateManager.get_state_summary()
            st.json(state_info)

        with col3:
            st.markdown("**Quick Actions**")

            if st.button("Clear Session", key="clear_session_btn"):
                SessionStateManager.clear()
                st.rerun()

            if st.button("Skip to Processing", key="skip_to_processing"):
                # Load valid mock data
                load_mock_data("valid")
                # Set to processing state
                SessionStateManager.set_current_state("processing")
                st.rerun()

            if st.button("Skip to Complete", key="skip_to_complete"):
                # Load valid mock data and output files
                load_mock_data("valid")
                load_mock_output_files()
                SessionStateManager.set_current_state("complete")
                st.rerun()


def load_mock_data(scenario: str = "valid"):
    """Load mock data for testing"""

    # Set mock scenario
    SessionStateManager.set("mock_scenario", scenario)
    SessionStateManager.set("use_mock_data", True)

    # Create mock files
    if scenario == "valid":
        template_df = MockDataProvider.get_mock_template_valid()
    elif scenario == "missing":
        template_df = MockDataProvider.get_mock_template_missing()
    elif scenario == "ignored":
        template_df = MockDataProvider.get_mock_template_ignored()
    else:  # mixed
        template_df = MockDataProvider.get_mock_template_missing()

    bulk_df = MockDataProvider.get_mock_bulk_data()

    # Create mock file objects
    from state.mock_data import MockFile

    template_file = MockFile("template_mock.xlsx", 125000)
    bulk_file = MockFile("bulk_mock.xlsx", 2300000)

    # Update session state
    SessionStateManager.set("template_file", template_file)
    SessionStateManager.set("bulk_file", bulk_file)
    SessionStateManager.set("template_df", template_df)
    SessionStateManager.set("bulk_df", bulk_df)
    SessionStateManager.set("cleaned_bulk_df", MockDataProvider.get_cleaned_bulk())
    SessionStateManager.set("validation_state", "pending")

    # Show success message
    st.success(f"Mock data loaded: {scenario} scenario")
    st.rerun()


def load_mock_output_files():
    """Load mock output files"""

    # Create mock output files
    working_file = MockDataProvider.create_mock_excel_file("working")
    clean_file = MockDataProvider.create_mock_excel_file("clean")

    # Generate filenames
    working_filename = MockDataProvider.generate_output_filename("Working")
    clean_filename = MockDataProvider.generate_output_filename("Clean")

    # Update session state
    SessionStateManager.update_output_files(
        working_file=working_file.getvalue(),
        clean_file=clean_file.getvalue(),
        working_filename=working_filename,
        clean_filename=clean_filename,
    )

    # Set processing stats
    SessionStateManager.update_processing_stats(MockDataProvider.get_processing_stats())

    # Set file stats
    SessionStateManager.set("file_stats", MockDataProvider.get_file_stats())
