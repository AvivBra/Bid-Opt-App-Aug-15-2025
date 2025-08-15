# פרק A2: פאנל Upload (3 שעות)

## עץ קבצים
```
bid-optimizer/
├── app/
│   └── ui/
│       ├── panels/
│       │   └── upload_panel.py    ✅
│       └── components/
│           ├── file_uploader.py   ✅
│           ├── checklist.py       ✅
│           └── buttons.py         ✅
└── data/
    └── template_generator.py      ✅
```

## מה המשתמש רואה
- **כפתור Download Template** - מוריד קובץ Excel עם 3 עמודות (Portfolio Name, Base Bid, Target CPA)
- **2 אזורי העלאה:**
  - "Upload Template (xlsx/csv)"
  - "Upload Bulk (xlsx/csv, sheet: Sponsored Products Campaigns)"
- **צ'קליסט 14 אופטימיזציות:**
  - Zero Sales (מסומן כברירת מחדל)
  - כרגע אין אופטימיזציות נוספות זה רק בהרחבה עתידית
- **סטטוס קבצים:** 
  - "Template: ✓" אחרי העלאה מוצלחת
  - "Bulk: ✓" אחרי העלאה מוצלחת
- **הודעת שגיאה:** "File exceeds 40MB" אם הקובץ גדול מדי

## קבצים ננעלים בסוף הפרק
- `upload_panel.py`
- `file_uploader.py` 
- `checklist.py`
- `template_generator.py`