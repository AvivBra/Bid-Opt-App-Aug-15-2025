# Test Scenarios & Test Plan

## Test Data Preparation

### Required Test Files

#### 1. Valid Test Files
```
tests/fixtures/valid/
├── bulk_complete.xlsx          # 10 portfolios, all valid
├── bulk_with_missing.xlsx      # 15 portfolios (5 not in template)
├── bulk_with_excess.xlsx       # 7 portfolios (3 in template)
├── template_complete.xlsx      # Matches bulk_complete
├── template_partial.xlsx       # Missing 5 portfolios
└── template_with_ignore.xlsx   # 3 portfolios marked "Ignore"
```

#### 2. Invalid Test Files
```
tests/fixtures/invalid/
├── bulk_wrong_headers.xlsx     # Missing required columns
├── bulk_wrong_sheet.xlsx       # No "Sponsored Products Campaigns"
├── bulk_oversized.txt          # 41MB dummy file
├── template_empty.xlsx         # Headers only, no data
└── wrong_format.txt            # Not Excel or CSV
```

#### 3. Edge Case Files
```
tests/fixtures/edge_cases/
├── bulk_500k_rows.xlsx         # Maximum rows
├── bulk_40mb.xlsx              # Maximum size (just under)
├── all_portfolios_ignore.xlsx  # All marked as ignore
└── special_characters.xlsx     # Unicode, symbols in names
```

---

## Manual Test Scenarios

### Scenario 1: Happy Path ✅
**Goal**: Complete flow without issues

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1 | Open application | Wide layout, title visible | |
| 1.2 | Download template | Template downloads with 3 columns | |
| 1.3 | Upload template_complete.xlsx | Success message | |
| 1.4 | Upload bulk_complete.xlsx | Success message | |
| 1.5 | Select "Zero Sales" | Checkbox checked | |
| 1.6 | Click Validate tab | Tab switches, no errors | |
| 2.1 | View validation | "No missing portfolios" | |
| 2.2 | Click Output tab | Tab switches | |
| 3.1 | Wait for processing | Progress indicator shows | |
| 3.2 | Download Working File | File downloads correctly | |
| 3.3 | Download Clean File | File downloads correctly | |
| 3.4 | Click New Processing | Returns to Step 1, state cleared | |

---

### Scenario 2: Missing Portfolios Loop 🔄
**Goal**: Test completion template flow

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1 | Upload template_partial.xlsx | Success | |
| 1.2 | Upload bulk_with_missing.xlsx | Success | |
| 1.3 | Go to Validate | Shows "5 missing portfolios" | |
| 2.1 | Download completion template | Contains 5 portfolio names | |
| 2.2 | Fill Base Bid values | (External action) | |
| 2.3 | Upload completed template | Accepted | |
| 2.4 | Check missing count | Shows "0 missing" | |
| 2.5 | Continue button appears | Enabled | |
| 2.6 | Click Continue | Proceeds to Step 3 | |

---

### Scenario 3: Excess Portfolios 📋
**Goal**: Handle excess portfolios

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1 | Upload template with 10 items | Success | |
| 1.2 | Upload bulk with 7 items | Success | |
| 2.1 | Go to Validate | Shows "3 excess portfolios" | |
| 2.2 | View excess list | Shows 3 portfolio names | |
| 2.3 | Click Copy to Clipboard | Success message | |
| 2.4 | Continue button visible | Enabled immediately | |

---

### Scenario 4: Mixed (Missing + Excess) 🔀
**Goal**: Handle both conditions

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2.1 | Upload files with both | Shows both missing and excess | |
| 2.2 | Download completion | Only missing portfolios included | |
| 2.3 | Complete and upload | Missing resolved | |
| 2.4 | Excess still showing | List remains visible | |
| 2.5 | Continue available | Button enabled | |

---

## Error Scenarios 🚫

### Error Test Cases

| Test ID | Test Case | Action | Expected Error | Code |
|---------|-----------|--------|----------------|------|
| E01 | File too large | Upload 41MB file | "File must not exceed 40MB" | S1-002 |
| E02 | Wrong format | Upload .txt file | "Must be Excel or CSV format" | S1-001 |
| E03 | Wrong headers | Upload wrong headers | "Titles are incorrect" | S1-003 |
| E04 | Empty template | Upload empty file | "Template does not contain data" | S2-002 |
| E05 | All ignore | All portfolios ignored | "All portfolios marked Ignore" | S2-005 |
| E06 | No sheet | Missing required sheet | "Sheet not found" | - |
| E07 | No files | Try to proceed without files | Validate tab disabled | - |
| E08 | No optimization | No checkbox selected | Cannot proceed | - |

---

## Performance Tests ⚡

### Load Tests

| Test | Condition | Metric | Target | Actual |
|------|-----------|--------|--------|--------|
| P01 | 500K rows processing | Time | <30 sec | |
| P02 | 40MB file upload | Time | <10 sec | |
| P03 | Memory usage (40MB) | RAM | <500MB | |
| P04 | Multiple downloads | Stability | No crash | |
| P05 | Rapid tab switching | Response | <1 sec | |

---

## Edge Cases 🔧

### Special Scenarios

| Test | Description | Expected Behavior |
|------|-------------|-------------------|
| Unicode | Portfolio names with émojis 🚀 | Handle correctly |
| Long names | 255 character portfolio names | Truncate/handle |
| Duplicates | Duplicate portfolio names | Process all |
| Case sensitivity | "Portfolio" vs "portfolio" | Case-sensitive match |
| Empty cells | Blank Base Bid values | Error on validation |
| Scientific notation | Large ID numbers | Preserve as text |
| Special chars | Names with &, %, $, @ | Handle correctly |

---

## Regression Tests 🔄

### After Each Change

- [ ] Happy path still works
- [ ] File size limit enforced
- [ ] Virtual Map freezes correctly
- [ ] Reset clears all state
- [ ] Downloads have correct names
- [ ] Error messages display properly

---

## UI/UX Tests 🎨

### Visual Checks

| Element | Check | Pass/Fail |
|---------|-------|-----------|
| Layout | Wide mode active | |
| Tabs | All 3 visible | |
| Colors | Error=Red, Warning=Yellow | |
| Pink notice | Shows in Step 3 | |
| Buttons | Primary=Blue, Secondary=Gray | |
| Spacing | Consistent padding | |
| Text | All English | |
| Icons | Display correctly | |

---

## Integration Test Flow

```python
# test_e2e_mockup.py

def test_complete_flow():
    """Test entire application flow"""
    
    # Step 1: Upload
    upload_valid_files()
    select_optimization()
    assert can_proceed_to_validate()
    
    # Step 2: Validate  
    check_portfolio_comparison()
    if has_missing():
        complete_missing_loop()
    assert can_proceed_to_output()
    
    # Step 3: Output
    wait_for_processing()
    download_files()
    assert files_valid()
    
    # Reset
    click_new_processing()
    assert state_cleared()
```

---

## Test Execution Checklist

### Before Release

#### Functional Tests
- [ ] All happy paths
- [ ] All error scenarios
- [ ] Missing portfolio loop (3 iterations)
- [ ] Excess portfolios handling
- [ ] Mixed scenario

#### Performance Tests
- [ ] 40MB file handling
- [ ] 500K rows processing
- [ ] Memory usage acceptable

#### UI Tests
- [ ] All buttons work
- [ ] All messages display
- [ ] Downloads function
- [ ] Reset works

#### Edge Cases
- [ ] Special characters
- [ ] Large numbers
- [ ] Empty values

#### Documentation
- [ ] README updated
- [ ] All code commented
- [ ] Test results documented

---

## Test Report Template

```markdown
## Test Execution Report
Date: ____
Version: Mockup v1.0
Tester: ____

### Summary
- Total Tests: ___
- Passed: ___
- Failed: ___
- Blocked: ___

### Failed Tests
| Test ID | Description | Issue | Severity |
|---------|-------------|-------|----------|

### Notes
[Any observations or recommendations]

### Sign-off
- [ ] Ready for deployment
- [ ] Requires fixes
```