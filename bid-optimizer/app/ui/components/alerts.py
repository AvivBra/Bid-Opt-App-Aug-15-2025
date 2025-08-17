# LOCKED - Phase A3 Complete
import streamlit as st


def get_theme_colors():
    """Get colors based on current theme"""
    is_dark = st.session_state.get("dark_mode", True)

    if is_dark:
        return {
            "bg": "#1A1D23",
            "border": "#2E3138",
            "text": "#FAFAFA",
            "success": "#00D26A",
            "error": "#FF6B6B",
            "info": "#6BB6FF",
            "warning": "#FFD68A",
            "pink": "#FFB4D0",
            "pink_border": "#FF4B9B",
            "violet": "#9B6BFF",
            "violet_hover": "#B589FF",
        }
    else:
        return {
            "bg": "#F8F9FA",
            "border": "#DEE2E6",
            "text": "#212529",
            "success": "#28A745",
            "error": "#DC3545",
            "info": "#007BFF",
            "warning": "#FFC107",
            "pink": "#E91E63",
            "pink_border": "#C2185B",
            "violet": "#9B6BFF",
            "violet_hover": "#B589FF",
        }


def render_success_alert(title: str, message: str = ""):
    """Render a success alert with green checkmark"""
    colors = get_theme_colors()

    alert_html = f"""
    <div style='background-color: {colors["bg"]}; border: 1px solid {colors["border"]}; 
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: {colors["success"]}; font-weight: bold;'>
            ✓ {title}
        </div>
        {f'<div style="color: {colors["text"]}; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_error_alert(title: str, message: str = ""):
    """Render an error alert with red X"""
    colors = get_theme_colors()

    alert_html = f"""
    <div style='background-color: {colors["bg"]}; border: 1px solid {colors["border"]}; 
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: {colors["error"]}; font-weight: bold;'>
            ❌ {title}
        </div>
        {f'<div style="color: {colors["text"]}; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_warning_alert(title: str, message: str = ""):
    """Render a warning alert"""
    colors = get_theme_colors()

    alert_html = f"""
    <div style='background-color: {colors["bg"]}; border: 1px solid {colors["border"]}; 
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: {colors["warning"]}; font-weight: bold;'>
            ⚠️ {title}
        </div>
        {f'<div style="color: {colors["text"]}; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_info_alert(title: str, message: str = ""):
    """Render an info alert"""
    colors = get_theme_colors()

    alert_html = f"""
    <div style='background-color: {colors["bg"]}; border: 1px solid {colors["border"]}; 
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: {colors["info"]}; font-weight: bold;'>
            ℹ️ {title}
        </div>
        {f'<div style="color: {colors["text"]}; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_pink_notice(title: str, message: str = ""):
    """Render a pink notice box for calculation errors"""
    colors = get_theme_colors()

    alert_html = f"""
    <div style='background-color: {colors["bg"]}; border: 2px solid {colors["pink_border"]};
                border-radius: 4px; padding: 16px; margin: 20px 0;'>
        <div style='color: {colors["pink"]}; font-weight: bold; font-size: 14px;'>
            Please note: {title}
        </div>
        {f'<div style="color: {colors["pink"]}; margin-top: 8px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_processing_spinner(message: str = "Processing..."):
    """Render a processing spinner with message"""
    colors = get_theme_colors()

    spinner_html = f"""
    <div style='text-align: center; padding: 20px;'>
        <div style='color: {colors["text"]}; margin-bottom: 10px;'>{message}</div>
        <div class='spinner'></div>
    </div>
    <style>
    .spinner {{
        border: 4px solid {colors["border"]};
        border-top: 4px solid {colors["violet"]};
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }}
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """
    st.markdown(spinner_html, unsafe_allow_html=True)
