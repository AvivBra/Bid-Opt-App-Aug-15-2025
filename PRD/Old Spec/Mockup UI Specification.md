# Mockup UI Specification

## Purpose
Create a **functional mockup** to validate the complete flow and UI design before implementing optimization logic.

## Mockup Structure
```
app/main.py              # Main entry point
app/ui/tabs/*.py         # Tab implementations
app/state/session.py     # State management
config/*.py              # Configuration files
```

## UI Mockup Components

### Global Settings
```python
st.set_page_config(
    page_title="Bid Optimizer - Bulk",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Header Section
- Title: "Bid Optimizer – Bulk File"
- Subtitle/description (optional)
- No breadcrumbs needed

### Tab Structure
```python
tab1, tab2, tab3 = st.tabs(["📤 Upload", "✅ Validate", "📥 Output"])
```

---

## Tab 1: Upload (Visual Elements)

### Layout
- **Two equal columns**: `col1, col2 = st.columns(2)`

### Column 1 - Files Section
```python
st.subheader("Files")

# Download Template Button
st.download_button(
    label="📥 Download Template",
    data=template_excel_bytes,
    file_name="template.xlsx",
    help="Download empty template file"
)

# Template Upload
st.file_uploader(
    "Upload Template (xlsx/csv)",
    type=['xlsx', 'csv'],
    key="template"
)

# Bulk Upload  
st.file_uploader(
    "Upload Bulk (xlsx/csv, sheet: Sponsored Products Campaigns)",
    type=['xlsx', 'csv'],
    key="bulk"
)
```

### Column 2 - Optimization Selection
```python
st.subheader("Optimization Types")

# Checkbox for Zero Sales
st.checkbox("Zero Sales", value=True)

# Success message example
st.success("✅ Files validated successfully")

# Error message example  
st.error("❌ File 'bulk.xlsx' titles are incorrect")
```

---

## Tab 2: Validate (Visual Elements)

### File Summary Section
```python
st.subheader("Validation Summary")

# File status cards
col1, col2 = st.columns(2)
with col1:
    st.info("**Template:** template.xlsx ✅")
with col2:
    st.info("**Bulk:** bulk.xlsx ✅")
```

### Missing Portfolios Section
```python
# Missing counter
st.metric("Missing Portfolios", "12")

# Download completion template
st.download_button(
    "📥 Download Completion Template",
    data=completion_bytes,
    file_name="completion_template.xlsx"
)
```

### Excess Portfolios Section
```python
st.warning("**Excess Portfolios (4):**")

# Excess list in a box
excess_list = """
- Portfolio_ABC
- Portfolio_DEF  
- Portfolio_GHI
- Portfolio_JKL
"""
st.code(excess_list, language=None)

# Copy button
st.button("📋 Copy to Clipboard")
```

### Navigation
```python
col1, col2 = st.columns([1, 5])
with col1:
    st.button("⬅️ Back")
with col2:
    st.button("Continue ➡️", type="primary")
```

---

## Tab 3: Output (Visual Elements)

### Status Section
```python
st.subheader("Output")

# Progress during processing
with st.spinner("Processing optimizations..."):
    time.sleep(2)  # Simulate processing

# Pink notice (special styling needed)
st.markdown(
    """
    <div style='background-color: #FFE4E1; padding: 10px; border-radius: 5px; color: #8B0000;'>
    📝 Please note: 7 calculation errors in Zero Sales optimization.
    </div>
    """,
    unsafe_allow_html=True
)

# Info message
st.info("ℹ️ Bids outside range: 3 rows with bid >1.25, 2 rows with bid <0.02")
```

### Download Section
```python
col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "📥 Download Working File",
        data=working_bytes,
        file_name="Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx",
        type="primary"
    )

with col2:
    st.download_button(
        "📥 Download Clean File",
        data=clean_bytes,
        file_name="Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx",
        type="primary"
    )

with col3:
    st.button("🔄 New Processing", type="secondary")
```

---

## Mockup Data Management

```python
# Use existing example files for testing
SAMPLE_BULK_FILE = "Bulk File Example.xlsx"
SAMPLE_TEMPLATE_FILE = "Empty Template Example.xlsx"

# Sample data for displays
SAMPLE_PORTFOLIOS = [
    "Kids-Brand-US",
    "Kids-Brand-EU", 
    "Supplements-US",
    "Supplements-EU"
]

SAMPLE_ERRORS = {
    "wrong_titles": "File 'bulk.xlsx' titles are incorrect",
    "too_big": "File 'large.xlsx' must not exceed 40MB",
    "empty": "Template does not contain data"
}

SAMPLE_METRICS = {
    "missing_count": 12,
    "excess_count": 4,
    "calc_errors": 7,
    "high_bids": 3,
    "low_bids": 2
}
```

---

## Styling Notes

### Colors (Streamlit defaults)
- **Error**: Red (#FF4B4B)
- **Warning**: Yellow/Orange (#FFA500)
- **Success**: Green (#00CC00)
- **Info**: Blue (#0068C9)
- **Pink Notice**: Custom HTML (#FFE4E1 background)
- **Primary Buttons**: Red (#ff2b2b) - as configured in config.toml

### Layout
- Always use `layout="wide"`
- Consistent padding/spacing
- Clear visual hierarchy

### Interactive Elements
- Primary buttons: Red, prominent
- Secondary buttons: Gray, subtle
- Disabled state: Grayed out

---

## Mockup Interactions (Functional)

1. **Tab Navigation**: Click to switch (built-in)
2. **File Upload**: Real file processing
3. **Download Buttons**: Generate and download real files
4. **Checkboxes**: Update session state
5. **Copy Button**: Copy to clipboard functionality
6. **New Processing**: Clear session and restart
7. **Mockup Scenario Selector**: Test different validation scenarios (KEEP THIS!)

---

## Testing the Mockup

### Desktop View
- [ ] All elements visible
- [ ] Proper column layout
- [ ] Readable text size

### Responsive Check  
- [ ] Narrow window handling
- [ ] Mobile simulation
- [ ] Tab navigation works

### Visual Consistency
- [ ] Colors match spec
- [ ] Spacing consistent
- [ ] Fonts readable
- [ ] Icons clear

### Functional Testing
- [ ] Real file upload/download
- [ ] Session state management
- [ ] Virtual Map functionality
- [ ] Completion template loop

---

## Next Steps After Mockup Completion

1. **Mockup complete?** → Test all scenarios
2. **All scenarios work?** → Proceed to optimization logic
3. **Issues found?** → Fix and retest