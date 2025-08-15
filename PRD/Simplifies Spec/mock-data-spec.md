# Mock Data Specification - Bid Optimizer

## 1. Mock Session State

### Initial State
```python
MOCK_INITIAL_STATE = {
    'current_state': 'upload',
    'template_file': None,
    'bulk_file': None,
    'selected_optimizations': [],
    'validation_result': None,
    'output_files': None
}
```

### After Upload State
```python
MOCK_UPLOADED_STATE = {
    'current_state': 'validate',
    'template_file': MockFile('template.xlsx', 125_000),
    'bulk_file': MockFile('bulk.xlsx', 2_300_000),
    'selected_optimizations': ['Zero Sales'],
    'template_df': MOCK_TEMPLATE_DF,
    'bulk_df': MOCK_BULK_DF
}
```

### After Validation State
```python
MOCK_VALIDATED_STATE = {
    'current_state': 'ready',
    'validation_result': {
        'is_valid': True,
        'missing_portfolios': [],
        'messages': ['All portfolios valid']
    }
}
```

## 2. Mock Template Data

### Valid Template
```python
MOCK_TEMPLATE_DF = pd.DataFrame({
    'Portfolio Name': [
        'Kids-Brand-US',
        'Kids-Brand-EU', 
        'Supplements-US',
        'Supplements-EU',
        'Electronics-US'
    ],
    'Base Bid': [1.25, 0.95, 2.10, 1.85, 'Ignore'],
    'Target CPA': [5.00, 4.50, 8.00, 7.50, None]
})
```

### Template with Issues
```python
MOCK_TEMPLATE_MISSING = pd.DataFrame({
    'Portfolio Name': [
        'Kids-Brand-US',
        'Kids-Brand-EU'
    ],
    'Base Bid': [1.25, 0.95],
    'Target CPA': [5.00, 4.50]
})
# Missing: Supplements-US, Supplements-EU
```

## 3. Mock Bulk Data

### Sample Bulk Data (5 rows for demo)
```python
MOCK_BULK_DF = pd.DataFrame({
    'Product': ['ASIN123', 'ASIN456', 'ASIN789', 'ASIN012', 'ASIN345'],
    'Entity': ['Keyword', 'Product Targeting', 'Keyword', 'Campaign', 'Keyword'],
    'Operation': ['Create', 'Update', 'Create', 'Update', 'Create'],
    'Campaign ID': ['1234567890'] * 5,
    'Ad Group ID': ['9876543210'] * 5,
    'Portfolio ID': ['1111111111'] * 5,
    'Portfolio Name (Informational only)': [
        'Kids-Brand-US', 'Kids-Brand-US', 'Kids-Brand-EU',
        'Supplements-US', 'Supplements-EU'
    ],
    'State': ['enabled', 'enabled', 'enabled', 'paused', 'enabled'],
    'Campaign State (Informational only)': ['enabled'] * 5,
    'Ad Group State (Informational only)': ['enabled'] * 5,
    'Bid': [1.25, 0.95, 1.10, 2.00, 0.85],
    'Sales': [0, 150.00, 0, 500.00, 0],
    'Impressions': [1500, 3000, 2000, 5000, 1000],
    'Clicks': [15, 45, 10, 125, 5],
    'Spend': [18.75, 42.75, 11.00, 250.00, 4.25],
    'ACOS': [0, 28.5, 0, 50.0, 0],
    'ROAS': [0, 3.51, 0, 2.00, 0],
    # ... (other 30 columns with mock values)
})
```

### Cleaned Bulk (after filtering)
```python
MOCK_CLEANED_BULK = MOCK_BULK_DF[
    (MOCK_BULK_DF['Entity'].isin(['Keyword', 'Product Targeting'])) &
    (MOCK_BULK_DF['State'] == 'enabled')
]
# Results in 3 rows
```

## 4. Mock Validation Scenarios

### Scenario 1: All Valid
```python
MOCK_VALIDATION_VALID = {
    'is_valid': True,
    'missing_portfolios': [],
    'excess_portfolios': [],
    'messages': ['✓ All portfolios valid'],
    'errors': []
}
```

### Scenario 2: Missing Portfolios
```python
MOCK_VALIDATION_MISSING = {
    'is_valid': False,
    'missing_portfolios': ['Electronics-Global', 'Toys-US'],
    'excess_portfolios': [],
    'messages': ['Missing portfolios found'],
    'errors': ['Missing portfolios: Electronics-Global, Toys-US']
}
```

### Scenario 3: Mixed Issues
```python
MOCK_VALIDATION_MIXED = {
    'is_valid': False,
    'missing_portfolios': ['NewProduct-US'],
    'excess_portfolios': ['OldProduct-EU'],
    'messages': ['Portfolio mismatch found'],
    'errors': ['Missing: 1, Excess: 1']
}
```

## 5. Mock File Objects

### MockFile Class
```python
class MockFile:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    def read(self):
        return b'Mock file content'
    
    def getvalue(self):
        return b'Mock file content'
```

### Mock Downloads
```python
def create_mock_excel():
    """Create mock Excel file for download"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        MOCK_BULK_DF.to_excel(writer, sheet_name='Clean Zero Sales', index=False)
        MOCK_BULK_DF.to_excel(writer, sheet_name='Working Zero Sales', index=False)
    output.seek(0)
    return output
```

## 6. Mock Progress States

### Upload Progress
```python
UPLOAD_PROGRESS_STATES = [
    "Reading file...",
    "Validating structure...",
    "Checking columns...",
    "Complete!"
]
```

### Validation Progress
```python
VALIDATION_PROGRESS_STATES = [
    "Cleaning Bulk data...",
    "Extracting portfolios...",
    "Comparing with Template...",
    "Validation complete!"
]
```

### Processing Progress
```python
PROCESSING_PROGRESS_STATES = [
    "Initializing optimizations...",
    "Applying Zero Sales...",
    "Generating Working file...",
    "Generating Clean file...",
    "Processing complete!"
]
```

## 7. Mock Statistics

### Processing Stats
```python
MOCK_PROCESSING_STATS = {
    'total_rows': 1234,
    'rows_modified': 456,
    'calculation_errors': 7,
    'bids_out_of_range': {
        'high': 3,  # > 1.25
        'low': 2    # < 0.02
    },
    'processing_time': '2.3 seconds',
    'optimizations_applied': ['Zero Sales']
}
```

### File Stats
```python
MOCK_FILE_STATS = {
    'working_file': {
        'size': '2.4 MB',
        'sheets': 2,
        'rows': 1234
    },
    'clean_file': {
        'size': '1.8 MB',
        'sheets': 1,
        'rows': 1234
    }
}
```

## 8. Mock Error Messages

### File Errors
```python
MOCK_FILE_ERRORS = [
    "File exceeds 40MB limit",
    "File must be Excel (.xlsx) or CSV",
    "Sheet 'Sponsored Products Campaigns' not found",
    "Missing required columns: Campaign ID, Ad Group ID"
]
```

### Validation Errors
```python
MOCK_VALIDATION_ERRORS = [
    "Template is empty",
    "All portfolios marked as Ignore",
    "No valid rows after filtering",
    "Invalid Base Bid value in row 5"
]
```

## 9. Mock Timing

### Simulated Delays
```python
MOCK_DELAYS = {
    'file_read': 0.5,      # seconds
    'validation': 0.3,
    'cleaning': 0.4,
    'optimization': 1.0,
    'file_generation': 0.8
}
```

### Progress Simulation
```python
def simulate_progress(progress_bar, stages, delay=0.5):
    """Simulate progress through stages"""
    for i, stage in enumerate(stages):
        progress_bar.progress(
            (i + 1) / len(stages),
            text=stage
        )
        time.sleep(delay)
```

## 10. State Transitions

### State Machine Mock
```python
MOCK_STATE_TRANSITIONS = {
    'upload': {
        'next': 'validate',
        'condition': lambda s: s['template_file'] and s['bulk_file']
    },
    'validate': {
        'next': 'ready',
        'condition': lambda s: s['validation_result']['is_valid']
    },
    'ready': {
        'next': 'processing',
        'condition': lambda s: True
    },
    'processing': {
        'next': 'complete',
        'condition': lambda s: True
    },
    'complete': {
        'next': 'upload',
        'condition': lambda s: s.get('reset', False)
    }
}
```

## Usage in Development

### Phase A - UI Development
```python
# In upload_panel.py
if st.button("Upload"):
    st.session_state['template_file'] = MockFile('template.xlsx', 125_000)
    st.success("Template uploaded successfully")

# In validate_panel.py
if USE_MOCK_DATA:
    validation_result = MOCK_VALIDATION_VALID
else:
    validation_result = orchestrator.validate(...)
```

### Testing Different Scenarios
```python
# Scenario selector for testing
scenario = st.selectbox(
    "Test Scenario (Dev Only)",
    ["Valid", "Missing Portfolios", "File Too Large", "Wrong Columns"]
)

if scenario == "Missing Portfolios":
    st.session_state['validation_result'] = MOCK_VALIDATION_MISSING
```