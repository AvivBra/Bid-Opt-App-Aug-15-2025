# Zero Sales Optimization Specification

## Overview
Zero Sales optimization reduces bids for keywords and products with no sales (Units = 0), excluding specific portfolio types and handling Bidding Adjustments separately.

## Input Requirements

### From Template File
- **Portfolio Name** - for matching
- **Base Bid** - base bid value for calculations
- **Target CPA** - optional, affects calculation logic

### From Bulk File (48 columns)
Key columns used:
- **Entity** - must be "Keyword", "Product Targeting", or "Bidding Adjustment"
- **Campaign ID** - for matching Bidding Adjustments
- **Portfolio Name (Informational only)** - for filtering Flat portfolios
- **Campaign Name (Informational only)** - for "up and" detection
- **Units** - must be 0 for optimization
- **Clicks** - used in calculations
- **Percentage** - used for Max BA calculation
- **Bid** - the value to be optimized

## Processing Logic

### Step 1: Data Filtering

Filter rows where ALL conditions are met:
1. **Units = 0** - only rows with no unit sales
2. **Portfolio not Flat type** - exclude these portfolio names:
   - Flat 30
   - Flat 25
   - Flat 40
   - Flat 25 | Opt
   - Flat 30 | Opt
   - Flat 20
   - Flat 15
   - Flat 40 | Opt
   - Flat 20 | Opt
   - Flat 15 | Opt

### Step 2: Entity Separation

1. **Create separate sheet** for Entity = "Bidding Adjustment"
   - Sheet name: "Bidding Adjustment Zero Sales"
   - No helper columns added
   - No bid calculations performed

2. **Create separate sheet** for Entity = "Product Ad"
   - Sheet name: "Product Ad Zero Sales"
   - No helper columns added
   - No bid calculations performed
   - These rows are preserved as-is from the cleaning stage

3. **Main sheet** contains Entity = "Keyword" or "Product Targeting"
   - Sheet name: "Clean Zero Sales"
   - Helper columns added
   - Bid calculations performed

4. **Handle missing Bidding Adjustments**

5. **Handle missing Bidding Adjustments**
   - Show notification: "Note: No Bidding Adjustment rows found"
   - Set Max BA default value = 1

### Step 3: Helper Columns Addition

Add columns to the left of Bid column (main sheet only):

| Column | Calculation |
|--------|------------|
| **Max BA** | Maximum value from Percentage column where:<br>- Entity = "Bidding Adjustment"<br>- Campaign ID matches current row<br>- Default = 1 if no matches |
| **Base Bid** | Copy from Template by Portfolio Name |
| **Target CPA** | Copy from Template by Portfolio Name |
| **Adj. CPA** | Target CPA × (1 + Max BA/100) |
| **Old Bid** | Original Bid value (preserved) |
| **calc1** | See Cases C & D below |
| **calc2** | See Cases C & D below |

### Step 4: Bid Calculation

Four cases based on Target CPA presence and Campaign Name content:

#### Case A: No Target CPA + "up and" in Campaign Name
- **Condition:** Target CPA is empty AND Campaign Name contains "up and"
- **Formula:** Bid = Base Bid × 0.5

#### Case B: No Target CPA + No "up and" in Campaign Name  
- **Condition:** Target CPA is empty AND Campaign Name doesn't contain "up and"
- **Formula:** Bid = Base Bid

#### Case C: Has Target CPA + "up and" in Campaign Name
- **Condition:** Target CPA exists AND Campaign Name contains "up and"
- **Calculations:**
  - calc1 = Adj. CPA × 0.5 / (Clicks + 1)
  - calc2 = calc1 - Base Bid × 0.5
- **Bid Formula:**
  - If calc1 ≤ 0: Bid = calc2
  - If calc1 > 0: Bid = Base Bid × 0.5

#### Case D: Has Target CPA + No "up and" in Campaign Name
- **Condition:** Target CPA exists AND Campaign Name doesn't contain "up and"
- **Calculations:**
  - calc1 = Adj. CPA / (Clicks + 1)
  - calc2 = calc1 - Base Bid / (1 + Max BA / 100)
- **Bid Formula:**
  - If calc1 ≤ 0: Bid = calc2
  - If calc1 > 0: Bid = Base Bid / (1 + Max BA / 100)

### Step 5: Error Handling & Highlighting

1. **Pink highlighting** for rows where:
   - Bid < 0.02 (below minimum)
   - Bid > 1.25 (above maximum)
   - Bid calculation failed (formula error)

2. **User notification:**
   - "{X} rows below 0.02, {Y} rows above 1.25, {Z} rows with calculation errors"

## Output Structure

### Working File
**Filename:** `Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx`

**Sheets:**
1. "Clean Zero Sales" - Keywords/Product Targeting with all helper columns
2. "Bidding Adjustment Zero Sales" - Bidding Adjustments without modifications
3. "Working Zero Sales" - Same as Clean (reserved for future use)

### Clean File  
**Filename:** `Auto Optimized Bulk | Clean | YYYY-MM-DD | HH-MM.xlsx`

**Sheets:**
1. "Clean Zero Sales" - Keywords/Product Targeting with all helper columns
2. "Bidding Adjustment Zero Sales" - Bidding Adjustments without modifications

**Note:** Currently Working and Clean files are identical. In future versions, Clean file will exclude helper columns.

## Validation Points

### Pre-processing
- Check for Bidding Adjustment rows existence
- Verify Template portfolio matches
- Validate required columns exist

### Post-processing
- Count rows with bid violations
- Verify all rows have Operation = "Update"
- Confirm sheet structure is correct

## Performance Considerations

- Expected processing time: ~5 seconds per 10K rows
- Memory usage: ~200MB for 100K rows
- Maximum supported: 500K rows

## Error Messages

| Condition | Message |
|-----------|---------|
| No Bidding Adjustments | "Note: No Bidding Adjustment rows found" |
| Bid range violations | "{X} rows below 0.02, {Y} rows above 1.25" |
| Calculation errors | "{Z} rows with calculation errors" |
| Missing portfolio | "Portfolio '{name}' not found in Template" |

## Dependencies

- Template file must be validated before processing
- Bulk file must pass cleaning (Entity/State filters)
- Portfolio matching must be case-sensitive
- All calculations preserve original column order