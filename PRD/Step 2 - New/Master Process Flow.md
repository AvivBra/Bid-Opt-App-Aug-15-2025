# Step 2 - Validate Portfolios: Master Process Flow

## תנאי כניסה
- Template הועלה בהצלחה
- Bulk הועלה בהצלחה  
- סוג אופטימיזציה נבחר

## תרשים זרימה

```
[START Step 2]
    ↓
[1. יצירת Virtual Map ראשוני]
    ↓
[2. ניקוי ראשוני של Bulk]
    ↓
[3. השוואת פורטפוליוז]
    ↓
[4. בדיקת תוצאות]
    ├─[אין חסרים/עודפים] → [6. הקפאת Virtual Map]
    ├─[חסרים בלבד] → [5. לולאת השלמה]
    ├─[עודפים בלבד] → [הצגת עודפים] → [6. הקפאת Virtual Map]
    └─[חסרים + עודפים] → [הצגת עודפים] → [5. לולאת השלמה]
         ↓
[5. לולאת השלמת חסרים]
    ├─[5.1 יצירת Completion Template]
    ├─[5.2 העלאה ע"י משתמש]
    ├─[5.3 מיזוג ל-Virtual Map]
    └─[חזרה ל-3]
         ↓
[6. הקפאת Virtual Map + טריגור אוטומטי]
    ↓
[7. התחלת Step 3 אוטומטית]
    ├─[עיבוד נתונים]
    ├─[יצירת קבצי פלט]
    └─[מעבר אוטומטי לטאב Output]
    ↓
[END Step 2 / START Step 3]
```

## טבלת שלבים ומסמכי איפיון

| שלב | מסמך איפיון | מוכן |
|-----|-------------|------|
| 1. יצירת Virtual Map ראשוני | Step 2 - Initial Virtual Map Creation (Concise).md | ✓ |
| 2. ניקוי ראשוני של Bulk | Step 2 - Initial Bulk Cleanup (Concise).md | ✓ |
| 3. השוואת פורטפוליוז ובדיקת תוצאות | Step 2 - Portfolio Comparison (Concise).md | ✓ |
| 4.3 מיזוג Completion Template | Step 2 - Completion Template Merge (Concise).md | ✓ |
| 5. הקפאת Virtual Map | Step 2 - Virtual Map Freeze (Concise).md | ✓ |
| טיפול בשגיאות | Errors.md (קיים) | ✓ |

## טבלת שלבים וקבצי קוד

| שלב | קובץ קוד | פונקציה עיקרית |
|-----|----------|-----------------|
| 1. יצירת Virtual Map ראשוני | `app/ui/tabs/validate_tab.py` | `initialize_virtual_map()` |
| 2. ניקוי ראשוני של Bulk | `core/validate/bulk_cleanse.py` | `initial_cleanup()` |
| 3. השוואת פורטפוליוז ובדיקת תוצאות | `core/mapping/virtual_map.py` | `get_missing_portfolios()`, `get_excess_portfolios()` |
| 4.1 יצירת Completion Template | `core/io/writers.py` | `create_completion_template()` |
| 4.3 מיזוג ל-Virtual Map | `core/mapping/virtual_map.py` | `merge_completion_template()` |
| 5. הקפאת Virtual Map + טריגור | `core/mapping/virtual_map.py` | `freeze()` + טריגור Step 3 |
| 6. התחלת Step 3 אוטומטית | `app/ui/tabs/output_tab.py` | `process_optimizations()` |

## תנאי יציאה
- Virtual Map מלא וקפוא
- Bulk מנוקה
- **אין אפשרות חזרה - התהליך חד-כיווני**