# פרק A3: פאנל Validation (2 שעות)

## עץ קבצים
```
bid-optimizer/
├── app/
│   └── ui/
│       ├── panels/
│       │   └── validate_panel.py  ✅
│       └── components/
│           ├── alerts.py          ✅
│           └── portfolio_list.py  ✅
```

## מה המשתמש רואה
- **כותרת:** "Validation Results"
- **מצב תקין:**
  - "✓ All portfolios valid" (ירוק)
  - כפתור "Process Files" (אדום, פעיל)
- **מצב חסרים:**
  - "❌ Missing portfolios:" (אדום)
  - רשימת פורטפוליוז חסרים: "Port_A, Port_B, Port_C"
  - כפתור "Upload New Template" (אדום)
- **מצב Ignore:**
  - "ℹ️ Ignored portfolios: 3" (כחול)
- **אנימציית טעינה:** "Validating..." עם spinner

## קבצים ננעלים בסוף הפרק
- `validate_panel.py`
- `alerts.py`
- `portfolio_list.py`