# Data Flow - Bid Optimizer

## Overview - Simple Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   INPUTS    │ --> │  PROCESSING  │ --> │   OUTPUTS   │
└─────────────┘     └──────────────┘     └─────────────┘
     (2)                  (3)                   (2)
```

## Detailed Flow

```
                    USER UPLOADS
    ┌──────────────────┴──────────────────┐
    ▼                                      ▼
TEMPLATE.xlsx                          BULK.xlsx
(3 columns)                         (46 columns)
    │                                      │
    └──────────────┬───────────────────────┘
                   ▼
              VALIDATION
         ┌─────────────────┐
         │ 1. Check files  │
         │ 2. Clean Bulk   │
         │ 3. Compare      │
         └────────┬────────┘
                  ▼
            [Valid? Y/N]
               /     \
              /       \
           Yes         No --> Request new Template
            │
            ▼
        PROCESSING
    ┌───────────────┐
    │ Apply selected│
    │ optimizations│
    └───────┬───────┘
            │
    ┌───────┴────────┐
    ▼                ▼
WORKING.xlsx     CLEAN.xlsx
(all sheets)    (clean only)
```

## Step-by-Step Data Flow

### Step 1: INPUT
```
Template File                    Bulk File
     │                               │
     ▼                               ▼
Read Excel/CSV                 Read Excel/CSV
     │                               │
     ▼                               ▼
DataFrame (3 cols)            DataFrame (46 cols)
     │                               │
     └───────────┬───────────────────┘
                 ▼
            Session State
```

### Step 2: VALIDATION
```
         Session State
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
Check       Clean       Extract
Headers     Bulk        Portfolios
    │           │           │
    │      Filter by:       │
    │      - Entity         │
    │      - State          │
    │           │           │
    └───────────┼───────────┘
                ▼
         Compare Lists
                │
         ┌──────┴──────┐
         ▼             ▼
    All Match     Missing Found
         │             │
         │             ▼
         │         Show Error
         │         Request Fix
         ▼
    Ready to Process
```

### Step 3: PROCESSING
```
    Cleaned Bulk DataFrame
            │
            ▼
    For Each Selected Optimization:
    ┌─────────────────────┐
    │ 1. Read current data│
    │ 2. Apply logic      │
    │ 3. Update values    │
    │ 4. Track changes    │
    └──────────┬──────────┘
               ▼
        Modified DataFrame
               │
        ┌──────┴──────┐
        ▼             ▼
    Working        Clean
    Version       Version
    (2 sheets)    (1 sheet)
```

### Step 4: OUTPUT
```
    Modified DataFrames
            │
    ┌───────┴────────┐
    ▼                ▼
Working File     Clean File
    │                │
Add sheets:      Add sheets:
- Clean {opt}    - Clean {opt}
- Working {opt}      │
    │                │
    ▼                ▼
Excel Files with Dynamic Names:
"Auto Optimized Bulk | Type | Date | Time.xlsx"
```

## Data Transformations

### Template Data
```
INPUT:  Portfolio Name | Base Bid | Target CPA
        Campaign-A     | 1.25     | 5.00

STORED: Dictionary/DataFrame for lookup
        {
          'Campaign-A': {'base_bid': 1.25, 'target_cpa': 5.00}
        }
```

### Bulk Data Cleaning
```
INPUT:  1000 rows (all types)
        ▼
FILTER: Entity IN ('Keyword', 'Product Targeting')
        State = 'enabled'
        ▼
OUTPUT: 400 rows (filtered)
```

### Optimization Example (Zero Sales)
```
INPUT:  Row with Sales=0, Bid=1.00
        ▼
LOGIC:  if Sales == 0 and Impressions > 100:
           new_bid = bid * 0.5
        ▼
OUTPUT: Row with Sales=0, Bid=0.50, Operation="Update"
```

## File Size Flow

```
Template: ~1-10 KB
    ↓
Bulk: 1-40 MB
    ↓
Validation: In memory
    ↓
Processing: In memory
    ↓
Working File: ~1.5x Bulk size
Clean File: ~1x Bulk size
```

## Error Flow

```
Any Step Fails
      │
      ▼
Show Error Message
      │
      ▼
Stay at Current Step
      │
      ▼
User Fixes Issue
      │
      ▼
Retry Step
```

## State Management

```
┌─────────────────────────────────┐
│         SESSION STATE           │
├─────────────────────────────────┤
│ • template_file: BytesIO        │
│ • bulk_file: BytesIO            │
│ • template_df: DataFrame        │
│ • bulk_df: DataFrame            │
│ • cleaned_df: DataFrame         │
│ • validation_result: Dict       │
│ • selected_optimizations: List  │
│ • output_files: Dict            │
│ • current_state: String         │
└─────────────────────────────────┘
            ↑ ↓
    All components read/write
```

## Performance Considerations

```
10K rows:   ~5 seconds
100K rows:  ~30 seconds  
500K rows:  ~60 seconds

Memory Usage:
- Input: ~100MB for 100K rows
- Processing: ~200MB peak
- Output: ~150MB files
```