# פרק B1: קריאת קבצים (3 שעות)

## עץ קבצים
```
bid-optimizer/
├── data/
│   └── readers/
│       ├── __init__.py            ✅
│       ├── excel_reader.py        ✅
│       └── csv_reader.py          ✅
└── app/
    └── state/
        └── session.py             🔄 (חיבור לקוראים)
```

## מה המשתמש רואה
- **אותו UI בדיוק** - אבל עכשיו:
  - קבצים אמיתיים נקראים
  - מזהה נכון כותרות
  - מזהה sheet "Sponsored Products Campaigns"
  - סופר שורות אמיתיות
- **הודעות שגיאה אמיתיות:**
  - "Missing required columns: Campaign ID, Ad Group ID"
  - "Sheet 'Sponsored Products Campaigns' not found"

## קבצים ננעלים בסוף הפרק
- `excel_reader.py`
- `csv_reader.py`