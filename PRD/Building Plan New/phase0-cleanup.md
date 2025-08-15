# פרק 0 - ניקוי והכנה (2 שעות)

## מטרה
להכין סביבת עבודה נקייה ומאורגנת למוקאפ. למחוק כפילויות, לארגן את המבנה, ולוודא שהאפליקציה עדיין עולה לפני שמתחילים את הפיתוח.

## צקליסט בנייה

### משימה 1: גיבוי (5 דקות)
- [ ] יצירת תיקיית גיבוי: `backup_before_refactor_[תאריך]`
- [ ] העתקת כל הפרויקט לתיקיית הגיבוי
- [ ] וידוא שהגיבוי שלם (בדיקת גודל)

### משימה 2: מחיקת כפילויות (15 דקות)
```bash
# ביצוע המחיקות
- [ ] rm -rf app/pages/
- [ ] rm -rf services/file_io/
- [ ] rm services/virtual_map_service.py
- [ ] rm utils/session_manager.py
- [ ] rm -rf core/checklist/
- [ ] rm core/output/filenames.py
- [ ] rm __init__.py  # בשורש בלבד
```

### משימה 3: יצירת תיקיות חסרות (10 דקות)
```bash
- [ ] mkdir -p tests/fixtures/valid
- [ ] mkdir -p tests/fixtures/invalid
- [ ] mkdir -p tests/fixtures/edge_cases
- [ ] mkdir -p docs/development
```

### משימה 4: עדכון אימפורטים (20 דקות)
- [ ] חיפוש בכל הקבצים: `grep -r "services.file_io"`
- [ ] החלפה ל: `core.io`
- [ ] חיפוש: `grep -r "utils.session_manager"`
- [ ] החלפה ל: `app.state.session`
- [ ] חיפוש: `grep -r "services.virtual_map_service"`
- [ ] החלפה ל: `core.mapping.virtual_map`

### משימה 5: הוספת הערות TODO (10 דקות)
- [ ] פתיחת `core/mapping/virtual_map.py`
      הוספת: `# TODO: Critical - implement freeze/unfreeze logic`
- [ ] פתיחת `services/step2_service.py`
      הוספת: `# TODO: Critical - implement validation orchestration`
- [ ] פתיחת `app/ui/tabs/validate_tab.py`
      הוספת: `# TODO: Refactor - extract logic to service layer`

## צקליסט בדיקות משתמש

### בדיקה 1: האפליקציה עולה
**מה לעשות:**
1. פתח טרמינל
2. הרץ: `streamlit run app/main.py`
3. המתן לפתיחת הדפדפן

**תוצאה צפויה:**
- האפליקציה נפתחת בדפדפן
- נראים 3 טאבים: אפלואוד, ולידייט, אאוטפוט
- אין הודעות שגיאה אדומות
- הכפתורים אדומים (לא כחולים)

### בדיקה 2: טאב אפלואוד עובד
**מה לעשות:**
1. לחץ על טאב אפלואוד
2. לחץ על "Download Template"
3. בדוק שהקובץ ירד

**תוצאה צפויה:**
- כפתור הורדה עובד
- קובץ אקסל נשמר במחשב
- הקובץ מכיל 3 עמודות: Portfolio Name, Base Bid, Target CPA

### בדיקה 3: העלאת קבצים
**מה לעשות:**
1. העלה את הקובץ "Empty Template Example.xlsx"
2. העלה את הקובץ "Bulk File Example.xlsx"
3. סמן את הצקבוקס "Zero Sales"

**תוצאה צפויה:**
- שני הקבצים מתקבלים
- מופיעות הודעות ירוקות או כתומות
- הצקבוקס נשאר מסומן
- האפליקציה לא קורסת

## צקליסט בדיקות מפתח

### בדיקה 1: ספירת קבצים
```python
# test_file_count.py
import os

def test_deleted_files():
    """וידוא שהקבצים נמחקו"""
    assert not os.path.exists('app/pages/')
    assert not os.path.exists('services/file_io/')
    assert not os.path.exists('utils/session_manager.py')
    assert not os.path.exists('core/checklist/')
    print("✓ All files deleted successfully")

def test_empty_files_count():
    """ספירת קבצים ריקים"""
    empty_count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                if os.path.getsize(path) < 10:
                    empty_count += 1
    assert empty_count < 40, f"Too many empty files: {empty_count}"
    print(f"✓ Empty files: {empty_count}")
```

**תוצאה צפויה:**
- כל הבדיקות עוברות
- מספר הקבצים הריקים פחת

### בדיקה 2: אימפורטים
```python
# test_imports.py
def test_no_broken_imports():
    """בדיקה שאין אימפורטים שבורים"""
    try:
        from app.state import session
        from core.io import readers
        from core.mapping import virtual_map
        print("✓ All imports work")
    except ImportError as e:
        assert False, f"Import error: {e}"
```

**תוצאה צפויה:**
- כל האימפורטים עובדים
- אין שגיאות

### בדיקה 3: סטרימליט
```bash
# בדיקת סטרימליט
streamlit run app/main.py --logger.level=error
```

**תוצאה צפויה:**
- האפליקציה עולה
- אין שגיאות בקונסול
- ניתן לנווט בין הטאבים

## צקפוינט אמצע (שעה 1)
- [ ] כל הקבצים המיותרים נמחקו
- [ ] האפליקציה עדיין עולה
- [ ] אין שגיאות אימפורט
- [ ] מבנה התיקיות נקי

**אם נכשל:** חזור לגיבוי והתחל מחדש

## טיפול בבעיות נפוצות

### בעיה: ImportError אחרי מחיקה
**פתרון:**
```python
# חפש בכל הקבצים
grep -r "from services.file_io" .
# תקן ל:
from core.io import readers
```

### בעיה: סטרימליט לא עולה
**פתרון:**
```bash
# נקה קאש
streamlit cache clear
# בדוק לוגים
streamlit run app/main.py --logger.level=debug
```

### בעיה: טאב ולידייט קורס
**פתרון:**
זה צפוי! הלוגיקה עדיין חסרה. נתקן ביום 1.

## צקפוינט סיום (שעתיים)
- [ ] 7 קבצים/תיקיות נמחקו
- [ ] תיקיות טסטים נוצרו
- [ ] אימפורטים מעודכנים
- [ ] האפליקציה עולה ועובדת
- [ ] טאב אפלואוד פונקציונלי
- [ ] מבנה מוכן לפיתוח

## סיכום הפרק
**השגנו:**
- מבנה נקי ומאורגן
- הסרת כפילויות
- אפליקציה שעדיין עובדת

**מוכנים לפרק 1:**
- מבנה מוכן למימוש וירטואל מאפ
- ברור איפה הקבצים הקריטיים
- אין בלאגן של קבצים מיותרים

## חתימת סיום פרק 0
- [ ] תאריך: _______
- [ ] שעת התחלה: _______
- [ ] שעת סיום: _______
- [ ] קבצים שנמחקו: 7
- [ ] מבצע: _______