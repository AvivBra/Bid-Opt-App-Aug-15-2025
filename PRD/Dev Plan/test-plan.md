# Test Plan - Bid Optimizer

## 1. Test Strategy

### Levels of Testing
1. **Unit Tests** - Individual functions
2. **Integration Tests** - Module interactions
3. **E2E Tests** - Complete user flows
4. **User Acceptance Tests** - Real scenarios

### Test Environment
- **Development:** Mock data enabled
- **Testing:** Real files, controlled data
- **Production:** Real files, full validation

## 2. Unit Tests

### File Readers (data/readers/)
| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Read valid Excel | valid.xlsx | DataFrame with data |
| Read valid CSV | valid.csv | DataFrame with data |
| Read corrupt file | corrupt.xlsx | FileReadError |
| Read 41MB file | large.xlsx | FileSizeError |
| Missing sheet | no_sheet.xlsx | SheetNotFoundError |

### Validators (business/validators/)
| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Valid template | 3 columns, data | ValidationResult(valid=True) |
| Missing columns | 2 columns | ValidationResult(errors=['Missing columns']) |
| Empty template | 0 rows | ValidationResult(errors=['Empty file']) |
| Invalid Base Bid | "ABC" | ValidationResult(errors=['Invalid Base Bid']) |
| All Ignore | All "Ignore" | ValidationResult(errors=['All ignored']) |

### Optimizations (business/optimizations/)
| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Zero Sales logic | Sales=0, Impressions>100 | Bid reduced by 50% |
| Bid minimum | Bid=0.01 | Bid=0.02 (minimum) |
| Bid maximum | Bid=2.00 | Bid=1.25 (maximum) |
| Missing data | Sales=NaN | Skip row |

## 3. Integration Tests

### Upload → Validation Flow
```python
def test_upload_to_validation():
    # Upload files
    template = upload_template('test_template.xlsx')
    bulk = upload_bulk('test_bulk.xlsx')
    
    # Validate
    result = validate_files(template, bulk)
    
    # Assert
    assert result.is_valid
    assert len(result.missing_portfolios) == 0
```

### Validation → Processing Flow
```python
def test_validation_to_processing():
    # Setup valid state
    state = create_valid_state()
    
    # Process
    output = process_optimizations(state)
    
    # Assert
    assert 'working_file' in output
    assert 'clean_file' in output
```

## 4. End-to-End Test Scenarios

### Scenario 1: Happy Path
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open app | Upload section visible |
| 2 | Download template | Empty template downloaded |
| 3 | Upload filled template | "✓ Template uploaded" |
| 4 | Upload bulk file | "✓ Bulk uploaded" |
| 5 | Select Zero Sales | Checkbox checked |
| 6 | See validation | "✓ All portfolios valid" |
| 7 | Click Process | Progress bar appears |
| 8 | Download Working | File downloads with correct name |
| 9 | Download Clean | File downloads with correct name |
| 10 | Click Reset | Returns to step 1 |

### Scenario 2: Missing Portfolios
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1-4 | Upload files | Files uploaded |
| 5 | See validation | "Missing portfolios: ABC, DEF" |
| 6 | Upload new template | Can upload again |
| 7 | With all portfolios | "✓ All portfolios valid" |
| 8 | Continue to process | Works normally |

### Scenario 3: File Too Large
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Upload 41MB file | "File exceeds 40MB limit" |
| 2 | File not uploaded | State unchanged |
| 3 | Upload smaller file | Works normally |

### Scenario 4: Wrong Format
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Upload .txt file | "File must be Excel or CSV" |
| 2 | Upload .xls (old) | "File must be .xlsx format" |
| 3 | Upload .xlsx | Works normally |

## 5. Performance Tests

### Load Tests
| Test | Specification | Pass Criteria |
|------|--------------|---------------|
| 10K rows | Process time | < 5 seconds |
| 100K rows | Process time | < 30 seconds |
| 500K rows | Process time | < 60 seconds |
| optimization | Process time | < 120 seconds |

### Stress Tests
| Test | Action | Expected |
|------|--------|----------|
| Rapid clicks | Click Process 10 times | Only processes once |
| Multiple files | Upload 10 files rapidly | Handles gracefully |
| Browser refresh | Refresh mid-process | State preserved |

## 6. User Acceptance Tests

### Test Users
- **User A:** Experienced with Excel
- **User B:** New to bulk files
- **User C:** Power user (large files)

### Test Tasks
1. Upload files and process
2. Handle validation errors
3. Download and verify output
4. Use the optimization
5. Reset and start over

### Success Criteria
- Task completion rate > 90%
- No critical errors
- Output files correct
- User satisfaction > 4/5

## 7. Test Data Sets

### Valid Test Files
```
test_data/valid/
├── template_complete.xlsx       # All portfolios
├── template_with_ignore.xlsx    # Some ignored
├── bulk_small.xlsx              # 100 rows
├── bulk_medium.xlsx             # 10K rows
├── bulk_large.xlsx              # 100K rows
└── bulk_maximum.xlsx            # 499K rows
```

### Invalid Test Files
```
test_data/invalid/
├── template_empty.xlsx          # No data rows
├── template_wrong_columns.xlsx  # Wrong headers
├── template_all_ignore.xlsx     # All ignored
├── bulk_no_sheet.xlsx           # Missing sheet
├── bulk_wrong_columns.xlsx      # Missing columns
├── bulk_over_limit.xlsx         # 500K+ rows
└── file_corrupted.xlsx          # Corrupted
```

### Edge Cases
```
test_data/edge_cases/
├── special_characters.xlsx      # Portfolio names with #@$
├── unicode_names.xlsx           # Hebrew/Arabic names
├── extreme_values.xlsx          # Bid=999, CPA=9999
├── many_portfolios.xlsx         # 500 portfolios
└── single_row.xlsx              # Only 1 data row
```

## 8. Regression Tests

### After Each Change
1. Happy path still works
2. File size limit enforced
3. Download names correct
4. Reset clears everything
5. All 14 optimizations run

### Critical Functions
```python
# Must always pass
def test_critical_functions():
    assert validate_file_size(40_000_000) == True
    assert validate_file_size(40_000_001) == False
    assert clean_bulk_data(df).count() > 0
    assert generate_filename('Working') contains date
```

## 9. Test Automation

### Automated Tests
```python
# Run before each commit
pytest tests/unit/
pytest tests/integration/

# Run before release
pytest tests/e2e/
pytest tests/performance/
```

### Manual Tests
- UI visual inspection
- Download file opening
- Cross-browser testing
- User acceptance

## 10. Bug Report Template

### Bug Information
```
Title: [Brief description]
Severity: Critical/High/Medium/Low
Environment: Dev/Test/Prod

Steps to Reproduce:
1. 
2. 
3. 

Expected Result:

Actual Result:

Screenshots/Logs:

Additional Info:
```

### Test Log Template
```
Date: YYYY-MM-DD
Tester: [Name]
Version: [App version]

Test Cases Executed: X/Y
Passed: X
Failed: Y

Failed Tests:
- [Test name]: [Reason]

Notes:
```

## 11. Exit Criteria

### Ready for Production
- [ ] All unit tests pass (100%)
- [ ] Integration tests pass (100%)
- [ ] E2E happy path works
- [ ] No critical bugs
- [ ] Performance targets met
- [ ] UAT sign-off received
- [ ] Documentation complete
- [ ] Error messages clear

## 12. Test Schedule

| Phase | Duration | Focus |
|-------|----------|-------|
| Unit Testing | 2 days | Individual functions |
| Integration | 1 day | Module interactions |
| E2E Testing | 2 days | User scenarios |
| Performance | 1 day | Load and stress |
| UAT | 2 days | User acceptance |
| Regression | 1 day | Final check |

**Total: 9 days testing**