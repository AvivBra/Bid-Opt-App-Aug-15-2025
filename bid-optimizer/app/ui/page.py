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
from state.mock_data import MockDataProvider, MockFile
from config.constants import DEBUG_MODE


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

    # Check if using mock data
    if SessionStateManager.get("use_mock_data"):
        # Get mock validation result stored earlier
        validation_result = SessionStateManager.get("mock_validation_result")

        if validation_result:
            # Update session state with mock validation
            SessionStateManager.update_validation_result(
                is_valid=validation_result["is_valid"],
                missing=validation_result.get("missing_portfolios"),
                ignored=validation_result.get("ignored_portfolios"),
                messages=validation_result.get("messages"),
            )

            # Update validation stats
            stats = SessionStateManager.get("mock_stats", {})
            SessionStateManager.set(
                "validation_stats",
                {
                    "total_portfolios": stats.get("template_portfolios", 0),
                    "valid_rows": stats.get("cleaned_rows", 0),
                    "filtered_rows": stats.get("original_rows", 0)
                    - stats.get("cleaned_rows", 0),
                },
            )

            # Update validation state
            if validation_result["is_valid"]:
                if validation_result.get("ignored_portfolios"):
                    SessionStateManager.set("validation_state", "ignored")
                else:
                    SessionStateManager.set("validation_state", "valid")
            else:
                SessionStateManager.set("validation_state", "missing")

            # If valid, transition to ready state
            if validation_result["is_valid"]:
                SessionStateManager.set_current_state("ready")

            return

    # If not using mock data, just set validation as pending
    # In real implementation, this would trigger actual validation
    SessionStateManager.set("validation_state", "pending")


def render_debug_controls():
    """Render debug controls for testing different scenarios"""

    with st.expander("🔧 Debug Controls (Dev Only)"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Load Mock Data**")

            # Scenario selector with descriptions
            scenarios = {
                "valid": "✅ Valid - All match",
                "missing": "❌ Missing - Blocked",
            }

            scenario = st.selectbox(
                "Select Scenario",
                options=list(scenarios.keys()),
                format_func=lambda x: scenarios[x],
                key="mock_scenario_selector",
                help="Choose a test scenario",
            )

            # Load mock data button
            if st.button("Load Mock Data", key="load_mock_btn"):
                load_mock_data_from_provider(scenario)

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
                load_mock_data_from_provider("valid")
                # Set to processing state
                SessionStateManager.set_current_state("processing")
                st.rerun()

            if st.button("Skip to Complete", key="skip_to_complete"):
                # Load valid mock data and output files
                load_mock_data_from_provider("valid")
                load_mock_output_files()
                SessionStateManager.set_current_state("complete")
                st.rerun()


def load_mock_data_from_provider(scenario_name: str = "valid"):
    """Load mock data from MockDataProvider"""

    # Get scenario data
    scenarios = MockDataProvider.get_mock_scenarios()
    scenario_data = scenarios.get(scenario_name, scenarios["valid"])

    # Create mock file objects
    template_file, bulk_file = MockDataProvider.create_scenario_files(scenario_name)

    # Create MockFile wrappers
    template_mock = MockFile(
        f"template_{scenario_name}.xlsx",
        len(template_file.getvalue()),
        template_file.getvalue(),
    )
    bulk_mock = MockFile(
        f"bulk_{scenario_name}.xlsx", len(bulk_file.getvalue()), bulk_file.getvalue()
    )

    # Update session state
    SessionStateManager.set("mock_scenario", scenario_name)
    SessionStateManager.set("use_mock_data", True)
    SessionStateManager.set("template_file", template_mock)
    SessionStateManager.set("bulk_file", bulk_mock)
    SessionStateManager.set("template_df", scenario_data["template_df"])
    SessionStateManager.set("bulk_df", scenario_data["bulk_df"])
    SessionStateManager.set("cleaned_bulk_df", scenario_data["cleaned_df"])
    SessionStateManager.set("validation_state", "pending")
    SessionStateManager.set(
        "mock_validation_result", scenario_data["validation_result"]
    )
    SessionStateManager.set("mock_stats", scenario_data["stats"])

    # Show success message with scenario details
    st.success(f"Mock data loaded: {scenario_data['name']}")

    # Show stats
    stats = scenario_data["stats"]
    st.info(
        f"📊 Template: {stats.get('template_portfolios', 0)} portfolios | "
        f"Bulk: {stats.get('original_rows', 0)} rows → "
        f"{stats.get('cleaned_rows', 0)} after cleaning"
    )

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
