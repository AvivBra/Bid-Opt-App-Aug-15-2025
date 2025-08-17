# מפרט טכני - Bid Optimizer

## 1. טכנולוגיות

### Python
- **גרסה:** 3.8+
- **סיבה:** תמיכה מלאה ב-Type Hints ו-Dataclasses

### ספריות עיקריות
```
streamlit==1.28.0      # ממשק משתמש
pandas==2.0.0          # עיבוד נתונים
openpyxl==3.1.0       # קריאת/כתיבת Excel
python-dateutil==2.8.2 # טיפול בתאריכים
```

### ספריות עזר
```
typing                 # Type hints
dataclasses           # Data models
io.BytesIO            # טיפול בקבצים בזיכרון
datetime              # תאריכים לשמות קבצים
```

## 2. מגבלות טכניות

### גודל קבצים
- **מקסימום:** 40MB
- **בדיקה:** לפני קריאה
- **הודעת שגיאה:** "File exceeds 40MB limit"

### מספר שורות
- **מקסימום:** 500,000 שורות
- **בדיקה:** אחרי קריאה
- **הודעת שגיאה:** "File contains more than 500,000 rows"

### פורמטים נתמכים
- **Excel:** .xlsx (לא .xls)
- **CSV:** UTF-8 encoded
- **Sheets:** "Sponsored Products Campaigns" חובה ב-Bulk

### עמודות נדרשות

**Template (3 עמודות):**
1. Portfolio Name
2. Base Bid
3. Target CPA

**Bulk (48 עמודות):**
Product, Entity, Operation, Campaign ID, Ad Group ID, Portfolio ID, Ad ID, Keyword ID, Product Targeting ID, Campaign Name, Ad Group Name, Campaign Name (Informational only), Ad Group Name (Informational only), Portfolio Name (Informational only), Start Date, End Date, Targeting Type, State, Campaign State (Informational only), Ad Group State (Informational only), Daily Budget, SKU, ASIN, Eligibility Status (Informational only), Reason for Ineligibility (Informational only), Ad Group Default Bid, Ad Group Default Bid (Informational only), Bid, Keyword Text, Native Language Keyword, Native Language Locale, Match Type, Bidding Strategy, Placement, Percentage, Product Targeting Expression, Resolved Product Targeting Expression (Informational only), Impressions, Clicks, Click-through Rate, Spend, Sales, Orders, Units, Conversion Rate, ACOS, CPC, ROAS

### לשוניות נוספות
- המערכת שומרת את לשונית "Portfolios" אם קיימת

## 3. דרישות סביבה

### מערכת הפעלה
- Windows 10+
- macOS 10.14+
- Linux (Ubuntu 18.04+)

### Python Environment
```bash
# יצירת סביבה
python -m venv venv

# הפעלה
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# התקנה
pip install -r requirements.txt
```

### Streamlit Configuration
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 40
enableCORS = false

[theme]
primaryColor = "#FF0000"
backgroundColor = "#FFFFFF"
```

## 4. ביצועים

### זמני עיבוד צפויים
| פעולה | 10K שורות | 100K שורות | 500K שורות |
|--------|-----------|-------------|--------------|
| קריאת קובץ | <1 שניה | 2-3 שניות | 10-15 שניות |
| ניקוי Bulk | <1 שניה | 1-2 שניות | 5-8 שניות |
| ולידציה | <1 שניה | <1 שניה | 1-2 שניות |
| אופטימיזציה אחת | <1 שניה | 2-3 שניות | 10-12 שניות |
| יצירת קבצי פלט | 1 שניה | 3-5 שניות | 15-20 שניות |

### ניהול זיכרון
- **שימוש מקסימלי:** ~2GB RAM ל-500K שורות
- **Garbage Collection:** אוטומטי אחרי כל שלב
- **File Buffers:** BytesIO בזיכרון, לא בדיסק

### Progress Indicators
```python
# מוצג למשתמש במהלך:
- קריאת קבצים > 10MB
- עיבוד > 50K שורות
- יצירת קבצי פלט
```

## 5. מבנה קבצי פלט

### Working File
```
שם: Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx
Sheets: 
- Clean {OptimizationName}
- Working {OptimizationName}
```

### Clean File
```
שם: Auto Optimized Bulk | Clean | YYYY-MM-DD | HH-MM.xlsx
Sheets:
- Clean {OptimizationName}
```

### תוכן השינויים
- כל השורות: Operation = "Update"
- ערכי Bid מעודכנים לפי האופטימיזציה
- Working sheets: עמודות עזר נוספות (בגרסה מלאה)

## 6. Logging

### רמות Log
```python
INFO: התחלה/סיום של כל שלב
WARNING: ערכים חריגים (Bid > 1.25 או < 0.02)
ERROR: כשלון בקריאת קובץ או עיבוד
```

### מיקום Logs
```
logs/
├── app_YYYY-MM-DD.log
└── errors_YYYY-MM-DD.log
```

## 7. בדיקות ביצועים

### Load Testing
- 500K שורות: חייב להסתיים תוך 60 שניות
- 14 אופטימיזציות במקביל: תוך 120 שניות
- 10 קבצים ברצף: ללא דליפת זיכרון

### Stress Testing
- קובץ 39.9MB: חייב לעבוד
- קובץ 40.1MB: חייב להידחות
- 499,999 שורות: חייב לעבוד
- 500,001 שורות: חייב להידחות

## 8. תאימות

### דפדפנים
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### רזולוציות מסך
- מינימום: 1366x768
- מומלץ: 1920x1080
- תמיכה ב-Mobile: לא

### קידוד
- קבצי קלט: UTF-8
- קבצי פלט: UTF-8
- תמיכה בעברית: לא (אנגלית בלבד)