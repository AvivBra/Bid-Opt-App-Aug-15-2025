# תוכנית פיתוח UI-First - Bid Optimizer

## שלב A: UI מלא עם Mock Data (2 ימים)

### פרק A1: שלד בסיסי (2 שעות)

**מה בונים:** שלד האפליקציה

**עץ קבצים:**
```
app/
├── main.py                    ✅
└── ui/
    ├── page.py                ✅
    └── layout.py              ✅
.streamlit/
└── config.toml                ✅
```

**מה המשתמש רואה:** עמוד ריק עם כותרת "Bid Optimizer"

---

### פרק A2: פאנל Upload (3 שעות)

**מה בונים:** אזור העלאת קבצים מלא

**עץ קבצים:**
```
app/
└── ui/
    ├── panels/
    │   └── upload_panel.py    ✅
    └── components/
        ├── file_uploader.py   ✅
        ├── checklist.py       ✅
        └── buttons.py         ✅
```

**מה המשתמש רואה:** 
- כפתור Download Template (עובד - מוריד קובץ ריק)
- 2 אזורי העלאה לקבצים (עובדים)
- צ'קליסט 14 אופטימיזציות (ניתן לסמן)
- סטטוס קבצים "Template: ✓" "Bulk: ✓"

---

### פרק A3: פאנל Validation (2 שעות)

**מה בונים:** אזור תוצאות ולידציה

**עץ קבצים:**
```
app/
└── ui/
    ├── panels/
    │   └── validate_panel.py  ✅
    └── components/
        ├── alerts.py          ✅
        └── portfolio_list.py  ✅
```

**מה המשתמש רואה:**
- הודעה "Validation Results" 
- מצב תקין: "✓ All portfolios valid"
- מצב שגיאה: "Missing portfolios: Port_A, Port_B"
- כפתור "Upload New Template" או "Process Files"

---

### פרק A4: פאנל Output (2 שעות)

**מה בונים:** אזור הורדות

**עץ קבצים:**
```
app/
└── ui/
    ├── panels/
    │   └── output_panel.py    ✅
    └── components/
        ├── progress_bar.py    ✅
        └── download_buttons.py ✅
```

**מה המשתמש רואה:**
- Progress bar במהלך עיבוד
- 2 כפתורי הורדה (Working File, Clean File)
- כפתור Reset
- הודעות Pink notice על שגיאות חישוב

---

### פרק A5: State Management (2 שעות)

**מה בונים:** ניהול מצב עם דאטה מוק

**עץ קבצים:**
```
app/
└── state/
    ├── session.py             ✅
    └── mock_data.py           ✅
config/
├── constants.py               ✅
└── ui_text.py                 ✅
```

**מה המשתמש רואה:** 
- כל ה-UI מגיב כמו אמיתי
- מעבר בין מצבים עובד
- אפשר לבדוק כל תרחיש עם נתוני דמה

---

## שלב B: החלפת Mock ללוגיקה אמיתית (3 ימים)

### פרק B1: קריאת קבצים (3 שעות)

**מה בונים:** קוראי Excel/CSV

**עץ קבצים:**
```
data/
└── readers/
    ├── __init__.py            ✅
    ├── excel_reader.py        ✅
    └── csv_reader.py          ✅
```

**מה המשתמש רואה:** אותו דבר - אבל עכשיו עם קבצים אמיתיים

---

### פרק B2: ולידציה (4 שעות)

**מה בונים:** בדיקות על הקבצים

**עץ קבצים:**
```
business/
├── validators/
│   ├── __init__.py            ✅
│   ├── file_validator.py      ✅
│   └── portfolio_validator.py ✅
└── processors/
    ├── __init__.py            ✅
    └── bulk_cleaner.py        ✅
```

**מה המשתמש רואה:** הודעות שגיאה אמיתיות לפי הבעיה

---

### פרק B3: יצירת קבצי פלט (3 שעות)

**מה בונים:** מחולל קבצים

**עץ קבצים:**
```
business/
└── processors/
    └── file_generator.py      ✅
data/
└── writers/
    ├── __init__.py            ✅
    └── output_writer.py       ✅
utils/
├── __init__.py                ✅
└── filename_generator.py      ✅
```

**מה המשתמש רואה:** קבצי Excel אמיתיים להורדה

---

### פרק B4: Zero Sales (2 שעות)

**מה בונים:** אופטימיזציה ראשונה

**עץ קבצים:**
```
business/
└── optimizations/
    ├── __init__.py            ✅
    ├── base.py                ✅
    └── zero_sales.py          ✅
```

**מה המשתמש רואה:** שינויים בקובץ הפלט לפי הלוגיקה

---

### פרק B5: אופטימיזציות נוספות (אופציונלי)

**מה בונים:** אופטימיזציות עתידיות לפי הצורך

**עץ קבצים:**
```
business/
└── optimizations/
    └── [קבצי אופטימיזציות עתידיות]
```

**מה המשתמש רואה:** כל אופטימיזציה נוספת שתיווסף

---

## סיכום מבנה סופי

```
bid-optimizer/
├── app/
│   ├── main.py
│   ├── state/
│   │   ├── session.py
│   │   └── mock_data.py
│   └── ui/
│       ├── page.py
│       ├── layout.py
│       ├── panels/
│       │   ├── upload_panel.py
│       │   ├── validate_panel.py
│       │   └── output_panel.py
│       └── components/
│           ├── file_uploader.py
│           ├── checklist.py
│           ├── buttons.py
│           ├── alerts.py
│           ├── portfolio_list.py
│           ├── progress_bar.py
│           └── download_buttons.py
├── business/
│   ├── validators/
│   │   ├── file_validator.py
│   │   └── portfolio_validator.py
│   ├── processors/
│   │   ├── bulk_cleaner.py
│   │   └── file_generator.py
│   └── optimizations/
│       ├── base.py
│       └── zero_sales.py
├── data/
│   ├── readers/
│   │   ├── excel_reader.py
│   │   └── csv_reader.py
│   └── writers/
│       └── output_writer.py
├── config/
│   ├── constants.py
│   └── ui_text.py
├── utils/
│   └── filename_generator.py
├── tests/
│   ├── unit/
│   │   ├── test_readers.py
│   │   ├── test_validators.py
│   │   └── test_optimizations.py
│   ├── integration/
│   │   ├── test_upload_flow.py
│   │   ├── test_validation_flow.py
│   │   └── test_processing_flow.py
│   └── fixtures/
│       ├── valid_template.xlsx
│       ├── valid_bulk.xlsx
│       └── [קבצי בדיקה נוספים]
└── .streamlit/
    └── config.toml
```

**יתרון מרכזי:** ה-UI ננעל אחרי יומיים ולא נוגעים בו יותר

**סה"כ:** 5 ימי עבודה
- 2 ימים: UI מלא
- 3 ימים: לוגיקה

**הערה:** המערכת פונקציונלית לחלוטין עם Zero Sales בלבד. אופטימיזציות נוספות הן אופציונליות לגמרי.