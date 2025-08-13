# UI Demo Specification

## Purpose
Create a **visual-only prototype** to validate the UI design before implementing any business logic.

## Demo File Structure
```
ui_demo.py          # Single file for entire UI demo
demo_data.py        # Hardcoded sample data
requirements.txt    # Minimal: streamlit, pandas
```

## UI Demo Components

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
    data=dummy_excel_bytes,
    file_name="template.xlsx",
    help="Demo template for mockup only"
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
    data=dummy_completion_bytes,
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
        data=dummy_working_bytes,
        file_name="Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx",
        type="primary"
    )

with col2:
    st.download_button(
        "📥 Download Clean File",
        data=dummy_clean_bytes,
        file_name="Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx",
        type="primary"
    )

with col3:
    st.button("🔄 New Processing", type="secondary")
```

---

## Demo Data (`demo_data.py`)

```python
# Dummy bytes for download buttons
dummy_excel_bytes = create_dummy_excel()  # Returns BytesIO

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

### Layout
- Always use `layout="wide"`
- Consistent padding/spacing
- Clear visual hierarchy

### Interactive Elements
- Primary buttons: Blue, prominent
- Secondary buttons: Gray, subtle
- Disabled state: Grayed out

---

## Demo Interactions (Simulated)

1. **Tab Navigation**: Click to switch (built-in)
2. **File Upload**: Visual only, no processing
3. **Download Buttons**: Download dummy files
4. **Checkboxes**: Visual state change only
5. **Copy Button**: Show success message
6. **New Processing**: Refresh page

---

## Testing the Demo

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

---

## Next Steps After Approval

1. **Approved?** → Proceed to Phase 2 (Infrastructure)
2. **Changes needed?** → Update demo → Review again
3. **Major changes?** → Update spec docs → Rebuild demo