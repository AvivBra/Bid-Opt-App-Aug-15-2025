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
- **שינויים בקובץ הפלט:**
  - עמודת Bid משתנה לפי הלוגיקה
  - rows עם Sales=0 מקבלים Bid חדש
- **הודעות ספציפיות:**
  - "Applied Zero Sales optimization to 234 rows"
  - Pink notice עם מספר שגיאות אמיתי
  - "15 rows with bid >1.25, 8 rows with bid <0.02"
- **Sheet names נכונים:**
  - "Clean Zero Sales"
  - "Working Zero Sales"

## קבצים ננעלים בסוף הפרק
- `base.py`
- `zero_sales.py`