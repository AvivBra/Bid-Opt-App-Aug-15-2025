# Error Messages - Bid Optimizer

## File Upload Errors (אדום)

```
❌ File exceeds 40MB limit
❌ File must be Excel (.xlsx) or CSV format
❌ Cannot read file - it may be corrupted
❌ File is empty - no data found
❌ Required sheet 'Sponsored Products Campaigns' not found
```

## Template Validation Errors (אדום)

```
❌ Missing required columns: Portfolio Name, Base Bid, Target CPA
❌ Columns must be in exact order: Portfolio Name, Base Bid, Target CPA
❌ Template has no data rows
❌ Portfolio Name cannot be empty in row {n}
❌ Invalid Base Bid value in row {n} - must be number or 'Ignore'
❌ Base Bid must be between 0.00 and 999.99
❌ Duplicate portfolio name: {name}
❌ All portfolios marked as 'Ignore' - cannot proceed
```

## Bulk Validation Errors (אדום)

```
❌ Missing required columns: {column_names}
❌ File contains more than 500,000 rows (found: {count})
❌ No valid rows after filtering - check Entity and State columns
❌ Bulk file has no data after removing disabled items
```

## Portfolio Comparison Errors (אדום)

```
❌ Missing portfolios found - Reupload Full Template
The following {count} portfolios are in Bulk but not in Template:

{portfolio_1}
{portfolio_2}
{portfolio_3}

Upload a new Template file with ALL missing portfolios to continue.
Uploading a new Template will reset the validation process.
```

## Processing Errors (אדום)

```
❌ Failed to apply {optimization_name} optimization
❌ Unable to generate output files
❌ Processing failed - please try again
❌ Memory error - file too large to process
```

## Warning Messages (כתום)

```
⚠️ {n} rows have Bid values above $1.25
⚠️ {n} rows have Bid values below $0.02
⚠️ Some portfolios marked as 'Ignore' will be skipped
⚠️ File contains special characters in portfolio names
⚠️ Large file detected - processing may take longer
⚠️ {n} rows skipped due to missing data
```

## Info Messages (כחול)

```
ℹ️ Processing {n} rows...
ℹ️ Applying {optimization_name} optimization
ℹ️ Ignored portfolios: {count}
ℹ️ Cleaning Bulk data (removing disabled items)
ℹ️ Generating output files...
ℹ️ File size: {size} MB
ℹ️ Rows after filtering: {count}
```

## Success Messages (ירוק)

```
✓ Template uploaded successfully ({size} KB)
✓ Bulk file uploaded successfully ({size} MB)
✓ All portfolios valid
✓ Validation complete - ready to process
✓ Processing complete
✓ Optimization applied successfully
✓ Files ready for download
✓ Reset complete - ready for new files
```

## Pink Notice Box (ורוד - שגיאות חישוב)

```
┌────────────────────────────────────────────────┐
│ Please note: {n} calculation errors in        │
│ {optimization_name} optimization               │
│                                                │
│ These rows were skipped due to:               │
│ • Division by zero                            │
│ • Missing required values                     │
│ • Invalid data format                         │
└────────────────────────────────────────────────┘
```

## Progress Messages

```
Uploading... {percent}%
Validating...
Comparing portfolios...
Processing optimizations... {percent}%
Generating Working file...
Generating Clean file...
Finalizing...
```

## Button States

```
[Process Files] - Disabled: "Upload both files first"
[Process Files] - Disabled: "Fix validation errors first"
[Download Working File] - Disabled: "Processing not complete"
[Reset] - Tooltip: "Clear all data and start over"
```

## File Status Indicators

```
Template: ✓ template.xlsx (125 KB)
Template: ✗ Not uploaded
Template: ⚠️ Has issues

Bulk: ✓ bulk.xlsx (2.3 MB)
Bulk: ✗ Not uploaded
Bulk: ⚠️ Has issues
```

## Optimization Checklist Messages

```
☑ Zero Sales (recommended)
☐ Portfolio Bid Optimization
☐ Budget Optimization
...

Note: Select at least one optimization to proceed
```

## Download Section Messages

```
Files generated:
• Working File: {size} MB ({sheet_count} sheets)
• Clean File: {size} MB ({sheet_count} sheets)

File names:
• Auto Optimized Bulk | Working | {date} | {time}.xlsx
• Auto Optimized Bulk | Clean | {date} | {time}.xlsx
```

## Edge Case Messages

```
❌ Session expired - please refresh the page
❌ Browser not supported - please use Chrome, Firefox, Safari, or Edge
❌ JavaScript must be enabled to use this application
⚠️ Slow connection detected - upload may take longer
ℹ️ Using cached data from previous session
```

## Tooltip/Help Messages

```
Download Template: "Download an empty template with required columns"
Upload Template: "Upload your filled template with portfolio Base Bids"
Upload Bulk: "Upload your Amazon Bulk file (must contain 'Sponsored Products Campaigns' sheet)"
Select Optimizations: "Choose which optimizations to apply to your data"
Process Files: "Start processing with selected optimizations"
Reset: "Clear all data and start over"
```