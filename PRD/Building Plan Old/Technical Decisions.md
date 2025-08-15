# Technical Decisions

## Core Architecture Decisions

### 1. State Management
**Decision**: Streamlit Session State
```python
# Why: Built-in, simple, reliable for single-user app
if 'processing_state' not in st.session_state:
    st.session_state.processing_state = ProcessingState()
```
**Not**: Singleton pattern (overkill for this use case)

### 2. File Handling
**Decision**: BytesIO for all in-memory operations
```python
# Keep everything in memory, no temp files
buffer = io.BytesIO()
df.to_excel(buffer, index=False)
buffer.seek(0)
```
**Not**: Temporary files on disk (security/cleanup issues)

### 3. Data Types & Scientific Notation
**Decision**: Force string type for ID columns
```python
# Prevent scientific notation for long IDs
dtypes = {
    'Campaign ID': str,
    'Ad Group ID': str,
    'Portfolio ID': str,
    # ... all ID columns
}
df = pd.read_excel(file, dtype=dtypes)
```

### 4. Excel Engine
**Decision**: openpyxl for all Excel operations
```python
# Why: Best compatibility, feature-complete
pd.read_excel(file, engine='openpyxl')
df.to_excel(buffer, engine='openpyxl')
```

### 5. Business Logic Separation
**Decision**: Service Layer Pattern for Step 2
```python
# UI Layer (validate_tab.py) - Only UI
def render():
    service = Step2Service()
    result = service.process()
    display_result(result)

# Service Layer (step2_service.py) - Business Logic
class Step2Service:
    def process(self):
        # All business logic here
```
**Why**: Clean separation, testability, maintainability
**Not**: Mixed logic in UI files (hard to test and maintain)

### 6. Iteration Management
**Decision**: Centralized counter in Service
```python
class Step2Service:
    MAX_ITERATIONS = 10
    
    def __init__(self):
        self.iteration_count = 0
    
    def check_iteration_limit(self):
        if self.iteration_count >= self.MAX_ITERATIONS:
            raise MaxIterationsError()
```
**Why**: Required by spec, prevents infinite loops
**Not**: No limit (risk of infinite loop)

---

## Error Handling Strategy

### Error Display Hierarchy
1. **Critical Errors** (Red) - Block progress
   - Use: `st.error()`
   - Example: Wrong file format, file too large

2. **Warnings** (Yellow) - Allow progress
   - Use: `st.warning()`  
   - Example: Excess portfolios detected

3. **Info** (Blue) - Neutral information
   - Use: `st.info()`
   - Example: File upload successful

4. **Special Notices** (Pink) - Calculation issues
   - Use: Custom HTML
   - Example: Optimization errors in Step 3

### Error Codes Structure
```yaml
# errors/messages.yaml
S1-001:
  severity: error
  message: "File '{filename}' must be in Excel or CSV format"
  
S1-002:
  severity: error
  message: "File '{filename}' must not exceed 40MB"
```

---

## Performance Decisions

### File Size Limits
```python
MAX_FILE_SIZE = 40 * 1024 * 1024  # 40MB in bytes
MAX_ROWS = 500_000

# Check before processing
if uploaded_file.size > MAX_FILE_SIZE:
    raise FileTooLargeError
```

### Chunking Strategy
```python
# For large files, process in chunks
CHUNK_SIZE = 10_000
for chunk in pd.read_excel(file, chunksize=CHUNK_SIZE):
    process_chunk(chunk)
```

### Memory Management
```python
# Clear large objects after use
del large_df
gc.collect()
```

---

## Debug Mode Implementation

### Debug Configuration
```python
# config/settings.py
DEBUG_MODE = False  # Toggle for development

# utils/debug_manager.py
def debug_print(filename: str, step: str, rows: int):
    if DEBUG_MODE:
        # DEBUG MODE
        print(f"🔍 DEBUG [{filename}] {step}: {rows} rows")
        # DEBUG MODE
```

### Debug Removal Strategy
1. Search for `# DEBUG MODE` comments
2. Delete entire blocks (3 lines)
3. Or use DEBUG_MODE flag

---

## UI/UX Technical Choices

### Tab Implementation
```python
# Use native Streamlit tabs (not custom)
tab1, tab2, tab3 = st.tabs(["Upload", "Validate", "Output"])
```

### Column Layouts
```python
# Consistent column ratios
col1, col2 = st.columns(2)  # Equal columns
col1, col2 = st.columns([1, 3])  # Weighted columns
```

### Layout Decision
- Centered layout (not wide)
- No sidebar
- Reason: Better readability, focused interface

### Button States
```python
# Disable based on conditions
button_disabled = not all_files_valid
st.button("Continue", disabled=button_disabled)
```

---

## Virtual Map Design

### Structure
```python
@dataclass
class VirtualMapEntry:
    portfolio_name: str
    base_bid: float
    target_cpa: Optional[float]
    is_ignored: bool = False

# In ProcessingState
virtual_map: Dict[str, VirtualMapEntry] = {}
```

### Freeze Mechanism
```python
class ProcessingState:
    def freeze_virtual_map(self):
        """Lock Virtual Map at Step 2 end"""
        self.virtual_map_frozen = True
        self.frozen_map_copy = deepcopy(self.virtual_map)
```

### Merge and Override Rules
```python
def merge_rules():
    """
    1. Override: New values completely override old ones
    2. Delete on Ignore: Base Bid="Ignore" removes portfolio
    3. Preserve unchanged: Portfolios not in Completion remain
    """
    
def validation_rules():
    """
    - Missing Base Bid → BlockingError
    - Invalid Target CPA → ValidationError  
    - Portfolio not in Bulk → NotFoundError
    """
```

---

## File Naming Convention

### Output Files
```python
def generate_filename(file_type: str, optimization_type: str) -> str:
    """
    Format: Auto Optimized Bulk | {type} | YYYY-MM-DD | HH-MM
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    return f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"
```

---

## Testing Strategy

### Test Data Location
```
tests/fixtures/
├── valid_bulk.xlsx
├── invalid_bulk_headers.xlsx
├── oversized_bulk.xlsx
├── template_complete.xlsx
└── template_with_ignore.xlsx
```

### Mocking Strategy
```python
# For UI testing without backend
USE_MOCK_DATA = True

if USE_MOCK_DATA:
    return mock_portfolio_comparison()
else:
    return real_portfolio_comparison()
```

---

## Dependencies Management

### Core Dependencies
```txt
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
pyyaml>=6.0
```

### Development Dependencies
```txt
pytest>=7.0.0
black>=23.0.0
mypy>=1.0.0
```

---

## Code Style Decisions

### Docstring Format
```python
def process_file(file: BytesIO) -> pd.DataFrame:
    """
    Process uploaded file and return DataFrame.
    
    Args:
        file: Uploaded file as BytesIO
        
    Returns:
        Processed DataFrame
        
    Raises:
        ValidationError: If file validation fails
    """
```

### Type Hints
```python
# Use throughout for clarity
from typing import Optional, Dict, List, Tuple
```

### Import Organization
```python
# Standard library
import os
import io

# Third party
import streamlit as st
import pandas as pd

# Local
from config import constants
from core.validate import bulk_cleanse
```

---

## Service Layer Architecture

### Service Responsibilities
```python
class Step2Service:
    """
    Orchestrates all Step 2 business logic:
    - Virtual Map management
    - Portfolio comparison
    - Completion template handling
    - Iteration management
    - State transitions
    """
```

### Data Flow
```
UI Layer → Service Layer → Core Logic → Data Layer
         ←               ←             ←
```

### Service Pattern Benefits
- Testability: Can test logic without UI
- Reusability: Logic can be called from anywhere
- Maintainability: Changes isolated to service
- Clarity: Clear separation of concerns

---

## Default Values & Limits

### Completion Loop Protection
- MAX_COMPLETION_LOOPS = 10 (prevents infinite loop)

### Excel Formatting Defaults
- DEFAULT_COLUMN_WIDTH = 15
- DEFAULT_NUMBER_FORMAT = '#,##0.000'
- DEFAULT_TEXT_ALIGNMENT = 'center'