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
    # בדיקת 46 עמודות
    expected_columns = [
        "Product", "Entity", "Operation", "Campaign ID", 
        "Ad Group ID", "Portfolio ID", "Ad ID", "Keyword ID",
        # ... כל 46 העמודות
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
| שדה | בדיקה | ערך תקין | הודעה |
|------|--------|-----------|---------|
| Entity | ערכים תקינים | Keyword, Product Targeting, Campaign, Ad Group | Info only |
| State | ערכים תקינים | enabled, paused, archived | Info only |
| Bid | טווח | 0.02-1.25 | Warning: "{n} bids outside range" |
| Budget | חיובי | > 0 | Warning: "Negative budgets found" |

## 4. ולידציות השוואה (Template vs Bulk)

### תהליך הניקוי והשוואה
```python
def clean_and_compare(bulk_df, template_df):
    # 1. ניקוי Bulk
    cleaned = bulk_df[
        (bulk_df['Entity'].isin(['Keyword', 'Product Targeting'])) &
        (bulk_df['State'] == 'enabled') &
        (bulk_df['Campaign State (Informational only)'] == 'enabled') &
        (bulk_df['Ad Group State (Informational only)'] == 'enabled')
    ]
    
    # 2. הסרת ignored
    ignored_portfolios = template_df[
        template_df['Base Bid'] == 'Ignore'
    ]['Portfolio Name'].tolist()
    
    cleaned = cleaned[
        ~cleaned['Portfolio Name (Informational only)'].isin(ignored_portfolios)
    ]
    
    # 3. השוואה
    bulk_portfolios = cleaned['Portfolio Name (Informational only)'].unique()
    template_portfolios = template_df[
        template_df['Base Bid'] != 'Ignore'
    ]['Portfolio Name'].tolist()
    
    missing = set(bulk_portfolios) - set(template_portfolios)
    
    return missing
```

### תוצאות השוואה
| מצב | תיאור | הודעה | פעולה |
|-----|--------|---------|---------|
| תקין | כל הפורטפוליוז קיימים | "✓ All portfolios valid" | אפשר Process |
| חסרים | פורטפוליוז בBulk אך לא בTemplate | "Missing portfolios: {list}" | דרוש Template חדש |
| ריק אחרי ניקוי | 0 שורות אחרי סינון | "No valid rows after filtering" | בדוק את הBulk |

## 5. ולידציות בזמן עיבוד

### בדיקות Pre-Processing
| בדיקה | תנאי | פעולה |
|--------|------|--------|
| זיכרון פנוי | < 100MB | Warning + המשך עם chunks |
| משך זמן | > 60 שניות | Show progress bar |
| נתונים תקינים | NaN values | Skip rows with warning |

### בדיקות Post-Processing
| בדיקה | תיאור | הודעה |
|--------|--------|---------|
| Calculation errors | שורות שנכשל חישוב | Pink: "7 calculation errors" |
| Out of range | Bid < 0.02 או > 1.25 | Info: "15 bids outside range" |
| No changes | אין שינויים | Warning: "No changes made" |

## 6. סדר הולידציות

### Upload Phase
1. בדיקת פורמט קובץ
2. בדיקת גודל
3. ניסיון קריאה
4. בדיקת מבנה (עמודות)
5. בדיקת נתונים

### Validation Phase
1. ניקוי Bulk
2. חילוץ portfolios
3. השוואה עם Template
4. בדיקת תוצאות

### Processing Phase
1. Pre-checks (זיכרון, נתונים)
2. Apply optimizations
3. Post-checks (שגיאות, טווחים)
4. Generate files

## 7. Error Recovery

### ולידציות עם Recovery
```python
def validate_with_recovery(file):
    try:
        # Try normal read
        df = pd.read_excel(file)
    except UnicodeDecodeError:
        # Try different encoding
        df = pd.read_excel(file, encoding='latin1')
    except Exception as e:
        # Last resort - try CSV
        try:
            df = pd.read_csv(file)
        except:
            raise FileReadError("Cannot read file in any format")
    
    return df
```

## 8. Performance Validations

### Timeout Settings
| פעולה | Timeout | פעולה בTimeout |
|--------|---------|----------------|
| קריאת קובץ | 30 שניות | Cancel + Error |
| ולידציה | 10 שניות | Continue with warning |
| עיבוד | 120 שניות | Show "Still working..." |
| יצירת פלט | 60 שניות | Retry once |

## 9. הודעות ולידציה לפי חומרה

### Critical (חוסם המשך)
- Missing required columns
- File too large
- All portfolios ignored
- No rows after filtering

### Warning (לא חוסם)
- Special characters in names
- Bids outside recommended range
- Large file (>20MB)
- Many portfolios (>100)

### Info (למידע בלבד)
- Number of rows processed
- Ignored portfolios count
- Optimization statistics

## 10. Custom Validations לכל אופטימיזציה

### Zero Sales
- בדיקה: יש עמודת Sales
- בדיקה: יש שורות עם Sales = 0

### Portfolio Bid
- בדיקה: יש Target CPA בTemplate
- בדיקה: Portfolio names match

### Budget Optimization
- בדיקה: יש עמודת Daily Budget
- בדיקה: Budget > 0

[וכן הלאה לכל 14 האופטימיזציות]