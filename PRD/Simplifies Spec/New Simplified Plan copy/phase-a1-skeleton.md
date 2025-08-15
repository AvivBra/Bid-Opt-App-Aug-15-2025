# פרק A1: שלד בסיסי (2 שעות)

## עץ קבצים
```
bid-optimizer/
├── app/
│   ├── main.py                    ✅
│   └── ui/
│       ├── page.py                ✅
│       └── layout.py              ✅
├── .streamlit/
│   └── config.toml                ✅
└── requirements.txt               ✅
```

## מה המשתמש רואה
- עמוד ריק עם כותרת "Bid Optimizer - Bulk File"
- 3 אזורים ריקים: Upload | Validate | Output
- רקע לבן, כפתורים אדומים (סטייל מוגדר)
- האפליקציה עולה ב-`streamlit run app/main.py`

## קבצים ננעלים בסוף הפרק
- `main.py` - נקודת כניסה
- `config.toml` - הגדרות Streamlit
- `requirements.txt` - רשימת ספריות