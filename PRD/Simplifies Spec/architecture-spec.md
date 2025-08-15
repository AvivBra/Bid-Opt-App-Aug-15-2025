# מפרט ארכיטקטורה - Bid Optimizer

## 1. עקרונות ארכיטקטוניים

### הפרדת אחריות (Separation of Concerns)
- **UI Layer:** תצוגה בלבד, ללא לוגיקה עסקית
- **Business Layer:** כל הלוגיקה העסקית והחישובים
- **Data Layer:** קריאה וכתיבה של קבצים בלבד

### כללי תקשורת
- UI ← Session State ← Business
- Business ← Data
- UI לעולם לא פונה ישירות ל-Data

## 2. ארכיטקטורת 3 שכבות

### שכבת UI (app/ui/)
**תפקיד:** ממשק משתמש וויזואליזציה
**רכיבים:**
- `page_single.py` - עמוד ראשי
- `panels/` - פאנלים לכל שלב
- `components/` - רכיבי UI לשימוש חוזר
- `layout.py` - עיצוב ופריסה

**כללים:**
- רק קריאה מ-Session State
- רק קריאה לפונקציות Orchestrator
- אין לוגיקת עיבוד נתונים

### שכבת Business Logic (business/)
**תפקיד:** לוגיקה עסקית וחישובים
**רכיבים:**
- `validators/` - ולידציות
- `processors/` - עיבוד נתונים
- `optimizations/` - 14 אופטימיזציות
- `services/orchestrator.py` - תיאום בין רכיבים

**כללים:**
- מקבל DataFrames, מחזיר DataFrames
- אין תלות ב-Streamlit
- ניתן לבדיקה בנפרד מה-UI

### שכבת Data Access (data/)
**תפקיד:** קריאה וכתיבה של קבצים
**רכיבים:**
- `readers/` - קריאת Excel/CSV
- `writers/` - כתיבת קבצי פלט
- `models/` - מבני נתונים

**כללים:**
- אין לוגיקה עסקית
- רק I/O operations
- מחזיר DataFrames או Exceptions

## 3. מבנה קבצים מלא

```
bid-optimizer/
├── app/
│   ├── main.py                    # נקודת כניסה
│   ├── ui/
│   │   ├── page_single.py         # עמוד ראשי
│   │   ├── panels/
│   │   │   ├── upload_panel.py    # פאנל העלאה
│   │   │   ├── validate_panel.py  # פאנל ולידציה
│   │   │   └── output_panel.py    # פאנל פלט
│   │   ├── components/
│   │   │   ├── checklist.py       # רשימת אופטימיזציות
│   │   │   ├── file_cards.py      # כרטיסי קבצים
│   │   │   ├── alerts.py          # הודעות
│   │   │   └── buttons.py         # כפתורים
│   │   └── layout.py               # פריסה
│   └── state/
│       └── session.py              # ניהול State
├── business/
│   ├── validators/
│   │   ├── template_validator.py  # ולידציית Template
│   │   └── bulk_validator.py      # ולידציית Bulk
│   ├── processors/
│   │   ├── optimizer.py           # מנהל אופטימיזציות
│   │   ├── file_generator.py      # יוצר קבצי פלט
│   │   └── optimizations/         # 14 אופטימיזציות
│   └── services/
│       └── orchestrator.py        # מתאם ראשי
├── data/
│   ├── readers/
│   │   ├── excel_reader.py        # קורא Excel
│   │   └── csv_reader.py          # קורא CSV
│   ├── writers/
│   │   └── output_writer.py       # כותב קבצי פלט
│   └── models/
│       ├── portfolio.py           # מודל Portfolio
│       └── validation_result.py   # תוצאות ולידציה
└── config/
    ├── constants.py                # קבועים
    ├── settings.py                 # הגדרות
    └── ui_text.py                  # טקסטים
```

## 4. זרימת נתונים (Data Flow)

### תהליך העלאה
```
User → UI (upload_panel) → Session State → Orchestrator → 
→ Excel/CSV Reader → DataFrame → Session State
```

### תהליך ולידציה
```
Session State → Orchestrator → Validators → 
→ ValidationResult → Session State → UI (validate_panel)
```

### תהליך עיבוד
```
Session State → Orchestrator → Optimizer → 
→ Each Optimization → Modified DataFrame → 
→ FileGenerator → OutputWriter → Excel Files
```

## 5. Session State Structure

```python
{
    # קבצים שהועלו
    'template_file': BytesIO,
    'bulk_file': BytesIO,
    
    # DataFrames
    'template_df': pd.DataFrame,
    'bulk_df': pd.DataFrame,
    'cleaned_bulk_df': pd.DataFrame,
    
    # תוצאות ולידציה
    'validation_result': {
        'is_valid': bool,
        'missing_portfolios': List[str],
        'messages': List[str]
    },
    
    # בחירות משתמש
    'selected_optimizations': List[str],
    
    # קבצי פלט
    'output_files': {
        'working': BytesIO,
        'clean': BytesIO
    },
    
    # מצב אפליקציה
    'current_state': 'upload' | 'validate' | 'process' | 'complete'
}
```

## 6. תקשורת בין שכבות

### UI → Business
- תמיד דרך Orchestrator
- פרמטרים: DataFrames או primitives
- החזרה: DataFrames או ValidationResult

### Business → Data
- ישירות לקוראים/כותבים
- פרמטרים: file paths או BytesIO
- החזרה: DataFrames או Exceptions

### מה שאסור
- UI → Data (ישירות)
- Data → Business (callback)
- Business → UI (ישירות)

## 7. עקרונות עיצוב

### Stateless Business Logic
- כל פונקציה מקבלת את כל הנתונים שהיא צריכה
- אין state פנימי ב-Business Layer
- ניתן לבדיקה עצמאית

### Single Responsibility
- כל מודול אחראי על דבר אחד
- כל אופטימיזציה בקובץ נפרד
- כל validator בקובץ נפרד

### Error Propagation
- Exceptions עולים מ-Data → Business → UI
- UI מציג הודעות ידידותיות
- Business לא תופס Exceptions מ-Data