# פרק B2: ולידציה (4 שעות)

## עץ קבצים
```
bid-optimizer/
├── business/
│   ├── validators/
│   │   ├── __init__.py            ✅
│   │   ├── file_validator.py      ✅
│   │   └── portfolio_validator.py ✅
│   └── processors/
│       ├── __init__.py            ✅
│       └── bulk_cleaner.py        ✅
└── app/
    └── state/
        └── session.py             🔄 (חיבור לולידטורים)
```

## מה המשתמש רואה
- **ולידציה אמיתית:**
  - סינון Bulk: Entity=Keyword/Product Targeting/Product Ad/Bidding Adjustment
  - הפרדה ל-3 לשוניות:
    - לשונית ראשית: Keyword + Product Targeting
    - לשונית Product Ad: Product Ad בלבד
    - לשונית Bidding Adjustment: Bidding Adjustment בלבד
  - ניקוי State רק בלשוניות ראשית ו-Product Ad (לא ב-Bidding Adjustment)
  - השוואת פורטפוליוז אמיתית
- **מספרים אמיתיים:**
  - "Missing portfolios (2): Port_ABC, Port_DEF" (מספר + שמות אמיתיים מהקובץ)
  - "1,234 rows after filtering (was 5,678)"
- **הודעות שגיאה ספציפיות:**
  - "Portfolio 'XYZ' has Base Bid='Ignore' - skipping"
  - "No rows left after filtering - check your Bulk file"

## קבצים ננעלים בסוף הפרק
- `file_validator.py`
- `portfolio_validator.py`
- `bulk_cleaner.py`