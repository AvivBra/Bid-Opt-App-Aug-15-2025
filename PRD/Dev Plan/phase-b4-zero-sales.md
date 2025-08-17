# פרק B4: Zero Sales (2 שעות)

## עץ קבצים
```
bid-optimizer/
├── business/
│   └── optimizations/
│       ├── __init__.py            ✅
│       ├── base.py                ✅
│       └── zero_sales.py          ✅
└── app/
    └── state/
        └── session.py             🔄 (חיבור לאופטימיזציות)
```

## מה המשתמש רואה

### שינויים בקובץ הפלט:
- **מבנה לשוניות:**
  - "Clean Zero Sales" - Keywords/Product Targeting עם עמודות עזר
  - "Bidding Adjustment Zero Sales" - Bidding Adjustments בלבד
  - "Working Zero Sales" - זהה ל-Clean (לעתיד)

- **עמודות עזר חדשות (משמאל ל-Bid):**
  - Max BA, Base Bid, Target CPA, Adj. CPA
  - Old Bid, calc1, calc2

- **שינויים בערכי Bid:**
  - שורות עם Units=0 מקבלים Bid חדש
  - 4 מקרים שונים לפי Target CPA ו-"up and"
  - שורות Bidding Adjustment לא משתנות

### הודעות ספציפיות:
- **הודעת מידע:** "Note: No Bidding Adjustment rows found" (אם רלוונטי)
- **הודעת סיכום:** "Applied Zero Sales optimization to 234 rows"
- **הודעת שגיאות:** "{X} rows below 0.02, {Y} rows above 1.25, {Z} rows with calculation errors"

### סימון חזותי:
- **צבע ורוד:** שורות עם Bid < 0.02 או > 1.25
- **צבע ורוד:** שורות עם שגיאת חישוב

### Sheet names נכונים:
- Working File: 3 sheets
- Clean File: 2 sheets

## קבצים ננעלים בסוף הפרק
- `base.py`
- `zero_sales.py`

## קריטריונים להצלחה
- [ ] סינון נכון לפי Units=0 ופורטפוליוז לא-Flat
- [ ] הפרדת Bidding Adjustment ללשונית נפרדת
- [ ] חישוב Max BA נכון מ-Percentage
- [ ] 4 מקרי החישוב עובדים נכון
- [ ] עמודות עזר מופיעות במקום הנכון
- [ ] סימון ורוד לערכים חריגים
- [ ] הודעות באנגלית בלבד