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
│   ├── main.py
│   ├── ui/
│   │   ├── page_single.py
│   │   ├── panels/
│   │   │   ├── __init__.py
│   │   │   ├── upload_panel.py
│   │   │   ├── validate_panel.py
│   │   │   └── output_panel.py
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── checklist.py
│   │   │   ├── file_cards.py
│   │   │   ├── alerts.py
│   │   │   └── buttons.py
│   │   └── layout.py
│   └── state/
│       ├── __init__.py
│       ├── session.py
│       └── mock_data.py
├── business/
│   ├── __init__.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── template_validator.py
│   │   └── bulk_validator.py
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── optimizer.py
│   │   ├── file_generator.py
│   │   └── optimizations/
│   │       ├── __init__.py
│   │       ├── base_optimization.py
│   │       └── zero_sales.py
│   └── services/
│       ├── __init__.py
│       └── orchestrator.py
├── data/
│   ├── __init__.py
│   ├── readers/
│   │   ├── __init__.py
│   │   ├── excel_reader.py
│   │   └── csv_reader.py
│   ├── writers/
│   │   ├── __init__.py
│   │   └── output_writer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── portfolio.py
│   │   └── validation_result.py
│   └── template_generator.py
├── config/
│   ├── __init__.py
│   ├── constants.py
│   ├── settings.py
│   └── ui_text.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   └── filename_generator.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_readers.py
│   │   ├── test_writers.py
│   │   ├── test_validators.py
│   │   ├── test_optimizations.py
│   │   ├── test_file_generator.py
│   │   └── test_orchestrator.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_upload_flow.py
│   │   ├── test_validation_flow.py
│   │   ├── test_processing_flow.py
│   │   └── test_end_to_end.py
│   ├── fixtures/
│   │   ├── valid_template.xlsx
│   │   ├── valid_bulk.xlsx
│   │   ├── invalid_template.xlsx
│   │   ├── invalid_bulk.xlsx
│   │   ├── large_bulk.xlsx
│   │   ├── empty_template.xlsx
│   │   └── missing_columns_bulk.xlsx
│   └── conftest.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
└── README.md


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