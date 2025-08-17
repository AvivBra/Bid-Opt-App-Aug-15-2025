# LOCKED - Phase A3 Complete
# LOCKED - Phase A3 Complete
import streamlit as st
from typing import List


def render_portfolio_list(portfolios: List[str], list_type: str = "Missing"):
    """
    Render a list of portfolios

    Args:
        portfolios: List of portfolio names
        list_type: Type of list (Missing/Ignored/Excess)
    """

    if not portfolios:
        return

    # Set color based on list type - brighter for dark mode
    color_map = {
        "Missing": "#FF6B6B",  # Bright Red
        "Ignored": "#6BB6FF",  # Bright Blue
        "Excess": "#FFD68A",  # Bright Yellow/Orange
        "Valid": "#00D26A",  # Bright Green
    }

    color = color_map.get(list_type, "#FAFAFA")

    # Create portfolio list HTML
    portfolio_items = "".join([f"<li>{portfolio}</li>" for portfolio in portfolios])

    list_html = f"""
    <div style='background-color: #262730; border-left: 4px solid {color};
                padding: 10px 15px; margin: 10px 0; border-radius: 4px;'>
        <ul style='margin: 0; padding-left: 20px; color: {color};'>
            {portfolio_items}
        </ul>
    </div>
    """

    st.markdown(list_html, unsafe_allow_html=True)


def render_portfolio_summary(
    total: int, valid: int, missing: int = 0, ignored: int = 0
):
    """
    Render a summary of portfolio validation

    Args:
        total: Total number of portfolios
        valid: Number of valid portfolios
        missing: Number of missing portfolios
        ignored: Number of ignored portfolios
    """

    # Calculate percentages
    valid_pct = (valid / total * 100) if total > 0 else 0
    missing_pct = (missing / total * 100) if total > 0 else 0
    ignored_pct = (ignored / total * 100) if total > 0 else 0

    summary_html = f"""
    <div style='background-color: #262730; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #333333;'>
        <h4 style='margin-top: 0; color: #FAFAFA;'>Portfolio Summary</h4>
        <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;'>
            <div>
                <span style='color: #B0B0B0;'>Total Portfolios:</span>
                <strong style='color: #FAFAFA; margin-left: 5px;'>{total}</strong>
            </div>
            <div>
                <span style='color: #00D26A;'>Valid:</span>
                <strong style='color: #00D26A; margin-left: 5px;'>{valid} ({
        valid_pct:.1f}%)</strong>
            </div>
            {
        f'''<div>
                <span style='color: #FF6B6B;'>Missing:</span>
                <strong style='color: #FF6B6B; margin-left: 5px;'>{missing} ({missing_pct:.1f}%)</strong>
            </div>'''
        if missing > 0
        else ""
    }
            {
        f'''<div>
                <span style='color: #6BB6FF;'>Ignored:</span>
                <strong style='color: #6BB6FF; margin-left: 5px;'>{ignored} ({ignored_pct:.1f}%)</strong>
            </div>'''
        if ignored > 0
        else ""
    }
        </div>
    </div>
    """

    st.markdown(summary_html, unsafe_allow_html=True)


def render_portfolio_table(portfolios_data: dict):
    """
    Render a table of portfolios with their status

    Args:
        portfolios_data: Dictionary with portfolio names as keys and status as values
    """

    if not portfolios_data:
        return

    # Start table HTML
    table_html = """
    <table style='width: 100%; border-collapse: collapse; margin: 15px 0;'>
        <thead>
            <tr style='background-color: #262730; border-bottom: 2px solid #333333;'>
                <th style='padding: 10px; text-align: left; color: #FAFAFA;'>Portfolio Name</th>
                <th style='padding: 10px; text-align: left; color: #FAFAFA;'>Status</th>
                <th style='padding: 10px; text-align: left; color: #FAFAFA;'>Base Bid</th>
            </tr>
        </thead>
        <tbody>
    """

    # Add rows
    for portfolio, data in portfolios_data.items():
        status = data.get("status", "Unknown")
        base_bid = data.get("base_bid", "-")

        # Set color based on status - brighter for dark mode
        status_color = {
            "Valid": "#00D26A",
            "Missing": "#FF6B6B",
            "Ignored": "#6BB6FF",
            "Invalid": "#FFD68A",
        }.get(status, "#B0B0B0")

        table_html += f"""
        <tr style='border-bottom: 1px solid #333333;'>
            <td style='padding: 8px; color: #FAFAFA;'>{portfolio}</td>
            <td style='padding: 8px;'>
                <span style='color: {status_color}; font-weight: bold;'>{status}</span>
            </td>
            <td style='padding: 8px; color: #FAFAFA;'>{base_bid}</td>
        </tr>
        """

    # Close table
    table_html += """
        </tbody>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)


def render_portfolio_pills(portfolios: List[str], max_display: int = 5):
    """
    Render portfolios as pills/badges

    Args:
        portfolios: List of portfolio names
        max_display: Maximum number to display before showing "+X more"
    """

    if not portfolios:
        return

    display_portfolios = portfolios[:max_display]
    remaining = len(portfolios) - max_display

    pills_html = (
        "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0;'>"
    )

    # Add portfolio pills
    for portfolio in display_portfolios:
        pills_html += f"""
        <span style='background-color: #333333; color: #FAFAFA; 
                     padding: 4px 12px; border-radius: 12px; font-size: 14px; border: 1px solid #444444;'>
            {portfolio}
        </span>
        """

    # Add "+X more" if needed
    if remaining > 0:
        pills_html += f"""
        <span style='background-color: #FF4B4B; color: white; 
                     padding: 4px 12px; border-radius: 12px; font-size: 14px;'>
            +{remaining} more
        </span>
        """

    pills_html += "</div>"

    st.markdown(pills_html, unsafe_allow_html=True)
