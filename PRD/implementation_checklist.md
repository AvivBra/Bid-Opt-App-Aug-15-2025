# Implementation Checklist

## 📋 Phase 0: UI Demo (CURRENT PRIORITY)

### Immediate Tasks
- [ ] Create `ui_demo.py` file
- [ ] Create `demo_data.py` with sample data
- [ ] Add basic `requirements.txt` (streamlit only)
- [ ] Run and test UI appearance
- [ ] Get stakeholder approval on visuals

**Hold Point**: ⏸️ Do not proceed past here without UI approval

---

## 📋 Phase 1: Project Setup

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] Create virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
  ```
- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

### Project Structure Creation
```bash
# Run these commands to create structure
mkdir -p app/ui/tabs app/pages app/state
mkdir -p core/io core/validate core/mapping core/output core/errors core/checklist
mkdir -p models services/file_io services/validation
mkdir -p optimizers/zero_sales/processors
mkdir -p utils templates docs tests/fixtures tests/unit tests/integration
mkdir -p config scripts
mkdir -p .streamlit
```

### Git Setup
- [ ] Initialize repository
  ```bash
  git init
  ```
- [ ] Create `.gitignore`
  ```
  *.pyc
  __pycache__/
  venv/
  .env
  .streamlit/secrets.toml
  *.xlsx
  !templates/*.xlsx
  .DS_Store
  ```
- [ ] Initial commit
  ```bash
  git add .
  git commit -m "Initial project structure"
  ```

---

## 📋 Phase 2: Configuration Files

### Core Config Files
- [ ] `config/constants.py`
  ```python
  # File limits
  MAX_FILE_SIZE_MB = 40
  MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
  MAX_ROWS = 500_000
  
  # Bid ranges (for reporting only in mockup)
  MIN_BID = 0.02
  MAX_BID = 1.25
  ```

- [ ] `config/settings.py`
  ```python
  # App settings
  APP_NAME = "Bid Optimizer - Bulk"
  DEBUG_MODE = False
  USE_MOCK_DATA = False  # For testing
  ```

- [ ] `config/ui_text.py`
  ```python
  # All UI strings in one place
  TITLE = "Bid Optimizer – Bulk File"
  TAB_UPLOAD = "Upload"
  TAB_VALIDATE = "Validate"
  TAB_OUTPUT = "Output"
  # ... etc
  ```

### Streamlit Config
- [ ] `.streamlit/config.toml`
  ```toml
  [theme]
  primaryColor = "#0068C9"
  backgroundColor = "#FFFFFF"
  secondaryBackgroundColor = "#F0F2F6"
  textColor = "#262730"
  
  [server]
  maxUploadSize = 40
  ```

---

## 📋 Phase 3: Base Templates & Files

### Template File
- [ ] `templates/empty_template.xlsx`
  - 3 columns: Portfolio Name, Base Bid, Target CPA
  - No data rows
  - Proper formatting

### Error Messages
- [ ] `core/errors/messages.yaml`
  ```yaml
  S1-001:
    severity: error
    message: "File '{filename}' must be in Excel or CSV format"
  S1-002:
    severity: error  
    message: "File '{filename}' must not exceed 40MB"
  # ... etc
  ```

---

## 📋 Phase 4: Core Models

### State Model
- [ ] `models/state.py`
  ```python
  @dataclass
  class ProcessingState:
      current_step: int = 1
      bulk_file: Optional[BytesIO] = None
      template_file: Optional[BytesIO] = None
      # ... etc
  ```

### File Schemas
- [ ] `models/file_schemas.py`
  - Bulk file columns definition
  - Template columns definition
  - Validation rules

### Portfolio Model
- [ ] `models/portfolio.py`
  ```python
  @dataclass
  class Portfolio:
      name: str
      base_bid: float
      target_cpa: Optional[float]
      is_ignored: bool = False
  ```

---

## 📋 Phase 5: Core Functions

### File I/O
- [ ] `core/io/readers.py` - Read Excel/CSV
- [ ] `core/io/writers.py` - Write Excel files
- [ ] `core/io/schema.py` - Verify headers

### Validation
- [ ] `core/validate/titles.py` - Header validation
- [ ] `core/validate/bulk_cleanse.py` - Initial cleanup
- [ ] `core/validate/portfolios.py` - Portfolio comparison

### Virtual Map
- [ ] `core/mapping/virtual_map.py` - Virtual Map management

### Output
- [ ] `core/output/files_builder.py` - Build output files
- [ ] `core/output/filenames.py` - Generate filenames

---

## 📋 Phase 6: UI Implementation

### Main App
- [ ] `app/main.py` - Entry point with tabs

### UI Components  
- [ ] `app/ui/layout.py` - Page config, headers
- [ ] `app/ui/widgets.py` - Reusable components
- [ ] `app/ui/messages.py` - Error/success messages
- [ ] `app/ui/style.py` - Custom styling

### Tab Logic
- [ ] `app/ui/tabs/upload_tab.py`
- [ ] `app/ui/tabs/validate_tab.py`
- [ ] `app/ui/tabs/output_tab.py`

### Pages (Entry Points)
- [ ] `app/pages/step1_upload.py`
- [ ] `app/pages/step2_validate.py`
- [ ] `app/pages/step3_output.py`

### Session Management
- [ ] `app/state/session.py` - State management

---

## 📋 Phase 7: Services Layer

### File Services
- [ ] `services/file_io/readers.py`
- [ ] `services/file_io/writers.py`

### Validation Services
- [ ] `services/validation/file_validator.py`
- [ ] `services/validation/data_validator.py`

### Portfolio Service
- [ ] `services/portfolio_service.py`

### Virtual Map Service
- [ ] `services/virtual_map_service.py`

---

## 📋 Phase 8: Optimizer (Mockup)

### Zero Sales Optimizer
- [ ] `optimizers/base.py` - Base interface
- [ ] `optimizers/zero_sales/optimizer.py` - Dummy implementation
- [ ] `optimizers/zero_sales/processors/sheet_creator.py`
- [ ] `optimizers/zero_sales/processors/data_cleaner.py`

---

## 📋 Phase 9: Utilities

### Utility Functions
- [ ] `utils/file_utils.py` - File helpers
- [ ] `utils/format_utils.py` - Display formatting
- [ ] `utils/session_manager.py` - Session helpers
- [ ] `utils/debug_manager.py` - Debug printing

---

## 📋 Phase 10: Testing

### Test Fixtures
- [ ] `tests/fixtures/sample_bulk.xlsx`
- [ ] `tests/fixtures/sample_template.xlsx`
- [ ] `tests/fixtures/large_bulk.xlsx` (40MB test)

### Unit Tests
- [ ] `tests/unit/test_schema.py`
- [ ] `tests/unit/test_bulk_cleanse.py`
- [ ] `tests/unit/test_portfolios_loop.py`
- [ ] `tests/unit/test_output_files.py`

### Integration Tests
- [ ] `tests/integration/test_e2e_mockup.py`

---

## 📋 Phase 11: Documentation

### User Documentation
- [ ] Update README.md with setup instructions
- [ ] Add usage examples
- [ ] Document known limitations

### Code Documentation
- [ ] Add docstrings to all functions
- [ ] Add type hints throughout
- [ ] Comment complex logic

---

## 📋 Phase 12: Final Steps

### Cleanup
- [ ] Remove all debug code
- [ ] Remove mock data flags
- [ ] Clean up imports

### Performance Check
- [ ] Test with 40MB file
- [ ] Test with 500K rows
- [ ] Check memory usage

### Final Testing
- [ ] Complete happy path test
- [ ] All error scenarios
- [ ] Reset functionality

### Deployment Prep
- [ ] Update requirements.txt
- [ ] Create run script
- [ ] Final commit

---

## 🎯 Definition of Done

### Mockup Complete When:
- [ ] All 3 steps functional
- [ ] File size limits enforced
- [ ] Virtual Map works correctly
- [ ] Completion loop tested
- [ ] Files downloadable
- [ ] Reset works properly
- [ ] No debug code remains
- [ ] All tests pass

---

## 📝 Notes

- Start with UI Demo (Phase 0)
- Get approval before proceeding
- Each phase builds on previous
- Test continuously
- Commit frequently