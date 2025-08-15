# LOCKED - Phase A3 Complete
# LOCKED - Phase A3 Complete
import streamlit as st


def render_success_alert(title: str, message: str = ""):
    """Render a success alert with green checkmark"""

    alert_html = f"""
    <div style='background-color: #d4edda; border: 1px solid #c3e6cb; 
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: #155724; font-weight: bold;'>
            ✓ {title}
        </div>
        {f'<div style="color: #155724; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_error_alert(title: str, message: str = ""):
    """Render an error alert with red X"""

    alert_html = f"""
    <div style='background-color: #f8d7da; border: 1px solid #f5c6cb;
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: #721c24; font-weight: bold;'>
            ❌ {title}
        </div>
        {f'<div style="color: #721c24; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_info_alert(title: str, message: str = ""):
    """Render an info alert with blue icon"""

    alert_html = f"""
    <div style='background-color: #d1ecf1; border: 1px solid #bee5eb;
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: #0c5460; font-weight: bold;'>
            ℹ️ {title}
        </div>
        {f'<div style="color: #0c5460; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_warning_alert(title: str, message: str = ""):
    """Render a warning alert with orange triangle"""

    alert_html = f"""
    <div style='background-color: #fff3cd; border: 1px solid #ffeaa7;
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: #856404; font-weight: bold;'>
            ⚠️ {title}
        </div>
        {f'<div style="color: #856404; margin-top: 4px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_pink_notice(title: str, message: str = ""):
    """Render a pink notice box for calculation errors"""

    alert_html = f"""
    <div style='background-color: #FFE4E1; border: 1px solid #FFB6C1;
                border-radius: 4px; padding: 16px; margin: 20px 0;'>
        <div style='color: #8B0000; font-weight: bold; font-size: 14px;'>
            Please note: {title}
        </div>
        {f'<div style="color: #8B0000; margin-top: 8px;">{message}</div>' if message else ""}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_processing_spinner(message: str = "Processing..."):
    """Render a processing spinner with message"""

    spinner_html = f"""
    <div style='text-align: center; padding: 20px;'>
        <div style='color: #666666; margin-bottom: 10px;'>{message}</div>
        <div class='spinner'></div>
    </div>
    <style>
    .spinner {{
        border: 4px solid #f3f3f3;
        border-top: 4px solid #FF0000;
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
