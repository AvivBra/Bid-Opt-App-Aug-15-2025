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
## מה המשתמש רואה
- **ולידציה אמיתית:**
  - סינון Bulk: Entity=Keyword/Product Targeting/Product Ad/Bidding Adjustment
  
- הפרדה ל-3 לשוניות:
  - **Targets**: Keyword + Product Targeting
  - **Product Ads**: Product Ad בלבד
  - **Bidding Adjustments**: Bidding Adjustment בלבד
- ניקוי State רק בלשוניות Targets ו-Product Ads (לא ב-Bidding Adjustments)
  
- **השוואת פורטפוליוז:**
  - מתבצעת רק על לשונית Targets
  - לא כוללת Product Ads או Bidding Adjustments
  - בודקת שכל פורטפוליו מ-Targets קיים ב-Template

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