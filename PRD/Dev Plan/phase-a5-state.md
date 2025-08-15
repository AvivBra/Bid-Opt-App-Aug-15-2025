# פרק A5: State Management (2 שעות)

## עץ קבצים
```
bid-optimizer/
├── app/
│   ├── ui/
│   │   └── page.py                🔄 (עדכון לחיבור state)
│   └── state/
│       ├── session.py             ✅
│       └── mock_data.py           ✅
└── config/
    ├── constants.py               ✅
    └── ui_text.py                 ✅
```

## מה המשתמש רואה
- **כל ה-UI מגיב כמו אמיתי:**
  - העלאת קובץ → מעבר למצב validated
  - לחיצה על Process → progress bar → הורדות זמינות
  - Reset → חזרה להתחלה
- **תרחישים שעובדים:**
  - תרחיש תקין (כל הפורטפוליוז קיימים)
  - תרחיש חסרים (3 פורטפוליוז חסרים)
  - תרחיש Ignore (2 פורטפוליוז ignored)
- **Mock files להורדה:**
  - קבצי Excel דמה נוצרים ומורדים

## קבצים ננעלים בסוף הפרק
- `session.py`
- `mock_data.py`
- `constants.py`
- `ui_text.py`
- `page.py` (גרסה סופית)

## 🔒 **סוף שלב A - כל ה-UI ננעל**