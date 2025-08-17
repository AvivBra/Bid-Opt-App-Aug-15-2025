import streamlit as st


def render_optimization_checklist():
    """Render optimization checklist"""

    # List of optimizations (defined locally to avoid import issues)
    optimizations = [
        "Zero Sales",
        "Portfolio Bid Optimization",
        "Budget Optimization",
        "Keyword Optimization",
        "ASIN Targeting",
        "Negative Keyword Optimization",
        "Placement Optimization",
        "Dayparting Optimization",
        "Search Term Optimization",
        "Product Targeting Optimization",
        "Campaign Structure Optimization",
        "Bid Adjustment Optimization",
        "Match Type Optimization",
        "Geographic Optimization",
    ]

    # Initialize selected_optimizations if not exists
    if "selected_optimizations" not in st.session_state:
        st.session_state.selected_optimizations = ["Zero Sales"]  # Default

    # Create 3 columns for nice display
    cols = st.columns(3)

    selected = []

    for i, opt in enumerate(optimizations):
        col_idx = i % 3
        with cols[col_idx]:
            # Set default value
            default_value = opt in st.session_state.selected_optimizations

            # Checkbox for each optimization
            if st.checkbox(
                opt, value=default_value, key=f"opt_{opt.replace(' ', '_').lower()}"
            ):
                selected.append(opt)

    # Update selections in session state
    st.session_state.selected_optimizations = selected

    # Add spacing before the info/warning messages
    st.markdown("<br>", unsafe_allow_html=True)

    # Warning if no optimization selected
    if not selected:
        st.warning("Please select at least one optimization to proceed")

    # Show count of selected optimizations
    if selected:
        st.info(f"{len(selected)} optimization(s) selected")
