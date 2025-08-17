# מפרט ולידציות - Bid Optimizer

## 1. ולידציות קבצים

### בדיקות גודל ופורמט
| בדיקה | תנאי | הודעת שגיאה |
|--------|------|--------------|
| גודל קובץ | > 40MB | "File exceeds 40MB limit" |
| פורמט קובץ | לא .xlsx או .csv | "File must be Excel (.xlsx) or CSV" |
| קובץ פגום | לא ניתן לקריאה | "Cannot read file - may be corrupted" |
| קובץ ריק | 0 שורות | "File is empty" |

### בדיקות Excel ספציפיות
| בדיקה | תנאי | הודעת שגיאה |
|--------|------|--------------|
| Sheet קיים | חסר "Sponsored Products Campaigns" | "Required sheet 'Sponsored Products Campaigns' not found" |
| Multi-sheet | יותר מ-sheet אחד בTemplate | "Template should have only one sheet" |

## 2. ולידציות Template

### בדיקת מבנה
```python
def validate_template_structure(df):
    # בדיקת עמודות
    required_columns = ["Portfolio Name", "Base Bid", "Target CPA"]
    if list(df.columns) != required_columns:
        return "Columns must be exactly: Portfolio Name, Base Bid, Target CPA"
    
    # בדיקת נתונים
    if len(df) == 0:
        return "Template has no data rows"
    
    return None  # תקין
```

### בדיקת ערכים
| שדה | בדיקה | ערכים תקינים | הודעת שגיאה |
|------|--------|---------------|--------------|
| Portfolio Name | לא ריק | כל טקסט | "Portfolio Name cannot be empty" |
| Portfolio Name | ללא כפילויות | ייחודי | "Duplicate portfolio: {name}" |
| Base Bid | חובה | מספר או "Ignore" | "Base Bid is required" |
| Base Bid | טווח | 0.00-999.99 או "Ignore" | "Base Bid must be 0-999.99 or 'Ignore'" |
| Target CPA | אופציונלי | 0.00-9999.99 או ריק | "Invalid Target CPA value" |

### בדיקות לוגיות
| בדיקה | תנאי | הודעת שגיאה |
|--------|------|--------------|
| All Ignore | כל Base Bid = "Ignore" | "All portfolios marked as Ignore - cannot proceed" |
| Special chars | תווים מיוחדים בשם | Warning: "Portfolio names contain special characters" |

## 3. ולידציות Bulk

### בדיקת מבנה
```python
def validate_bulk_structure(df):
    # בדיקת 48 עמודות
    expected_columns = [
        "Product", "Entity", "Operation", "Campaign ID", 
        "Ad Group ID", "Portfolio ID", "Ad ID", "Keyword ID",
        # ... כל 48 העמודות
    ]
    
    if list(df.columns) != expected_columns:
        missing = set(expected_columns) - set(df.columns)
        return f"Missing columns: {missing}"
    
    # בדיקת מספר שורות
    if len(df) > 500_000:
        return f"File has {len(df)} rows, maximum is 500,000"
    
    return None
```
### בדיקות נתונים

**בדיקת Entity:**
- ערכים תקינים: `Keyword`, `Product Targeting`, `Product Ad`, `Bidding Adjustment`, `Campaign`, `Ad Group`
- הודעה: Info only (המערכת לא דוחה, רק מסננת)

**בדיקת State:**
- ערכים תקינים: `enabled`, `paused`, `archived`
- הודעה: Info only (המערכת לא דוחה, רק מסננת)

**בדיקת Bid:**
- טווח תקין: 0.02-1.25
- הודעה: Warning - "{n} bids outside range"

**בדיקת Budget:**
- ערך תקין: חיובי (> 0)
- הודעה: Warning - "Negative budgets found"

### בדיקת Bidding Adjustment

**קיום Bidding Adjustment:**
- תנאי: 0 שורות עם Entity="Bidding Adjustment"
- הודעה: Info - "Note: No Bidding Adjustment rows found"

**ערכי Percentage:**
- תנאי: Percentage < 0 או > 900
- הודעה: Warning - "Unusual Percentage values detected"

### בדיקת Bidding Adjustment
| בדיקה | תנאי | הודעה |
|--------|------|---------|
| קיום Bidding Adjustment | 0 שורות עם Entity="Bidding Adjustment" | Info: "Note: No Bidding Adjustment rows found" |
| ערכי Percentage | Percentage < 0 או > 900 | Warning: "Unusual Percentage values detected" |

## 4. ולידציות השוואה (Template vs Bulk)

### תהליך הניקו

    def clean_and_separate(bulk_df, template_df):
        # שלב 1: סינון Entity
        entity_filter = bulk_df['Entity'].isin(['Keyword', 'Product Targeting', 'Product Ad', 'Bidding Adjustment'])
        filtered = bulk_df[entity_filter]
        
        # שלב 2: הפרדה ללשוניות
        targets_df = filtered[filtered['Entity'].isin(['Keyword', 'Product Targeting'])]
        product_ads_df = filtered[filtered['Entity'] == 'Product Ad']
        bidding_adjustments_df = filtered[filtered['Entity'] == 'Bidding Adjustment']
        
        # שלב 3: ניקוי נוסף - רק ללשוניות Targets ו-Product Ads
        # (Bidding Adjustments לא עובר ניקוי נוסף)
        state_filter = (
            (targets_df['State'] == 'enabled') &
            (targets_df['Campaign State (Informational only)'] == 'enabled') &
            (targets_df['Ad Group State (Informational only)'] == 'enabled')
        )
        targets_df_cleaned = targets_df[state_filter]
        
        product_ads_filter = (
            (product_ads_df['State'] == 'enabled') &
            (product_ads_df['Campaign State (Informational only)'] == 'enabled') &
            (product_ads_df['Ad Group State (Informational only)'] == 'enabled')
        )
        product_ads_df_cleaned = product_ads_df[product_ads_filter]
        
        # שלב 4: חילוץ פורטפוליוז מלשונית Targets בלבד
        bulk_portfolios = targets_df_cleaned['Portfolio Name (Informational only)'].unique()
        
        # שלב 5: חילוץ פורטפוליוז מ-Template (ללא Ignore)
        template_portfolios = template_df[
            template_df['Base Bid'].str.lower() != 'ignore'
        ]['Portfolio Name'].unique()
        
        # שלב 6: השוואה
        missing = set(bulk_portfolios) - set(template_portfolios)
        
        return {
            'targets': targets_df_cleaned,
            'product_ads': product_ads_df_cleaned,
            'bidding_adjustments': bidding_adjustments_df,  # לא עבר ניקוי נוסף
            'missing_portfolios': missing
        }


### תוצאות השוואה
| תרחיש | תוצאה | הודעה |
|---------|--------|---------|
| הכל תקין | 0 חסרים | "✓ All portfolios valid" |
| חסרים פורטפוליוז | N חסרים | "Missing portfolios: {names}" |
| כל הפורטפוליוז Ignore | - | "All portfolios marked as Ignore" |

## 5. ולידציות אופטימיזציה

### Zero Sales - לפני עיבוד
| בדיקה | תנאי | הודעה |
|--------|------|---------|
| Units column exists | חסרה עמודת Units | Error: "Units column required for Zero Sales" |
| Clicks column exists | חסרה עמודת Clicks | Error: "Clicks column required for Zero Sales" |
| Percentage column exists | חסרה עמודת Percentage | Warning: "Percentage column missing - Max BA will default to 1" |

### Zero Sales - אחרי עיבוד
| בדיקה | תנאי | הודעה |
|--------|------|---------|
| Bid range check | Bid < 0.02 | Pink highlight + count in message |
| Bid range check | Bid > 1.25 | Pink highlight + count in message |
| Calculation errors | NaN or null in Bid | Pink highlight + count in message |
| Final message | סיכום | "{X} rows below 0.02, {Y} rows above 1.25, {Z} rows with calculation errors" |

## 6. ולידציות קבצי פלט

### בדיקת מבנה
| בדיקה | תנאי | הודעת שגיאה |
|--------|------|--------------|
| Sheet count | פחות מהצפוי | "Missing output sheets" |
| Column count | לא 48 + עמודות עזר | "Invalid column structure" |
| Operation column | לא כל השורות "Update" | "Operation column not properly set" |

### בדיקת תוכן
| בדיקה | תנאי | הודעת שגיאה |
|--------|------|--------------|
| Empty sheets | 0 שורות | "Output sheet is empty" |
| Data integrity | מספר שורות לא תואם | "Row count mismatch" |
| Helper columns | חסרות עמודות עזר | "Helper columns missing" |

## 7. הודעות אזהרה (Warnings)

### Template Warnings
- "Portfolio names contain special characters"
- "Some Base Bid values are very high (>5.00)"
- "Many portfolios have no Target CPA"

### Bulk Warnings
- "Large file detected - processing may take longer"
- "Many disabled rows will be filtered out"
- "Note: No Bidding Adjustment rows found"

### Processing Warnings
- "Some calculations resulted in extreme bid values"
- "Many rows unchanged by optimization"
- "Processing time exceeded expectations"

## 8. סדר ביצוע ולידציות

```
1. File Validation
   ├── Size check
   ├── Format check
   └── Corruption check

2. Structure Validation
   ├── Column validation
   ├── Sheet validation
   └── Row count validation

3. Data Validation
   ├── Required fields
   ├── Data types
   └── Value ranges

4. Cross-file Validation
   ├── Portfolio matching
   ├── Bidding Adjustment check
   └── Consistency checks

5. Optimization Validation
   ├── Pre-processing checks
   ├── Calculation checks
   └── Post-processing checks

6. Output Validation
   ├── File structure
   ├── Data integrity
   └── Error highlighting
```