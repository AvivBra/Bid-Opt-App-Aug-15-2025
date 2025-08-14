# תוכנית פיתוח מוקאפ - Bid Optimizer

## מטרה
פיתוח מוקאפ פונקציונלי מלא של אפליקציית Bid Optimizer בשלושה שלבים (Upload, Validate, Output).
המוקאפ כולל את כל ה-UI והזרימה המלאה, אך ללא חישובי אופטימיזציה אמיתיים.

**חשוב**: זהו מוקאפ פונקציונלי מלא, לא דמו ויזואלי. האפליקציה צריכה לעבוד באמת - לקרוא קבצים, לנהל Virtual Map, וליצור קבצי output (זהים למקור במוקאפ).

## סטטוס נוכחי
האפליקציה נמצאת באמצע Phase 2 (תשתית וקבצי בסיס).

---

## Phase 1: מבנה פרויקט בסיסי ✅ הושלם 100%

### מה בוצע:
- ✅ מבנה תיקיות מלא
- ✅ קובץ `app/main.py` - נקודת כניסה ראשית
- ✅ שלושה טאבים: Upload, Validate, Output
- ✅ קבצי `__init__.py` בכל התיקיות
- ✅ קובץ `requirements.txt`
- ✅ תצורת Streamlit (`.streamlit/config.toml`)
- ✅ קבצי דוגמה: `Empty Template Example.xlsx`, `Bulk File Example.xlsx`

---

## Phase 2: תשתית וקבצי בסיס ✅ הושלם 90%

### מה בוצע:
- ✅ `config/settings.py` - הגדרות אפליקציה
- ✅ `config/constants.py` - קבועים (גדלי קבצים, עמודות נדרשות)
- ✅ `config/ui_text.py` - כל הטקסטים של ה-UI
- ✅ `app/state/session.py` - ניהול Session State מלא
- ✅ `app/ui/layout.py` - תצורת עמוד ופריסה (כולל CSS מותאם)
- ✅ `app/ui/widgets.py` - רכיבי UI לשימוש חוזר
- ✅ `app/ui/messages.py` - הודעות שגיאה/הצלחה/אזהרה (כולל pink notice)
- ✅ `app/ui/style.py` - עיצוב מלא (כפתורים אדומים, ללא אימוג'י, פריסה 1:6:1)

### מה חסר:
- ❌ `core/io/readers.py` - קריאת קבצי Excel/CSV
- ❌ `core/io/writers.py` - כתיבת קבצי Excel
- ❌ `core/validate/bulk_cleanse.py` - ניקוי ראשוני
- ❌ `core/mapping/virtual_map.py` - ניהול Virtual Map

---

## Phase 3: מימוש טאבים 🔄 הושלם 75-80%

### Upload Tab - ✅ הושלם 100%
- ✅ `app/ui/tabs/upload_tab.py` - מומש במלואו
- ✅ הורדת template ריק
- ✅ העלאת Template ו-Bulk
- ✅ בחירת Zero Sales
- ✅ הודעות סטטוס
- ✅ ולידציות ויזואליות

### Validate Tab - ✅ הושלם 80% (UI מלא, חסרה לוגיקה)
- ✅ `app/ui/tabs/validate_tab.py` - UI מלא ופונקציונלי
- ✅ **Mockup Scenario Selector** - חובה להשאיר! מאפשר בדיקת כל התרחישים
- ✅ תצוגת missing/excess portfolios
- ✅ כפתורי הורדה והעלאה
- ✅ מנגנון Copy to Clipboard
- ✅ לוגיקת מעבר בין מצבים
- ❌ **חסר**: לוגיקת Virtual Map אמיתית
- ❌ **חסר**: ניקוי ראשוני של Bulk
- ❌ **חסר**: השוואת פורטפוליוז אמיתית

### Output Tab - ✅ הושלם 75% (UI מלא, חסרה לוגיקה)
- ✅ `app/ui/tabs/output_tab.py` - UI מלא ופונקציונלי
- ✅ אנימציית עיבוד עם Progress Bar
- ✅ כפתורי הורדה (Working File, Clean File)
- ✅ Pink Notice לשגיאות חישוב
- ✅ הודעות Info על bids מחוץ לטווח
- ✅ סטטיסטיקות מוקאפ
- ✅ כפתור New Processing
- ❌ **חסר**: יצירת קבצי output אמיתיים
- ❌ **חסר**: שמות קבצים עם תאריך ושעה דינמיים

---

## Phase 4: לוגיקה בסיסית למוקאפ ⏳ טרם החל - **עדיפות עליונה**

### מה צריך לממש:

#### 1. קריאת וכתיבת קבצים - **קריטי**
```python
# core/io/readers.py
- read_excel(file) -> DataFrame
- read_csv(file) -> DataFrame
- validate_headers(df, required_columns) -> bool
- get_sheet(file, sheet_name) -> DataFrame

# core/io/writers.py
- create_excel(df, sheet_name) -> BytesIO
- create_multi_sheet_excel(sheets_dict) -> BytesIO
- create_template() -> BytesIO
- create_completion_template(missing_portfolios) -> BytesIO
```

#### 2. Virtual Map - **הלב של המערכת**
```python
# core/mapping/virtual_map.py
class VirtualMap:
    def __init__(self):
        self.data = {}  # {portfolio_name: {base_bid, target_cpa}}
        self.is_frozen = False
        
    def add_portfolio(name, base_bid, target_cpa=None):
        """הוספת פורטפוליו"""
        
    def remove_portfolio(name):
        """הסרת פורטפוליו (במקרה של Ignore)"""
        
    def merge_completion_template(df):
        """מיזוג עם דריסה מלאה"""
        
    def get_missing_portfolios(bulk_portfolios) -> list:
        """מציאת פורטפוליוז חסרים"""
        
    def get_excess_portfolios(bulk_portfolios) -> list:
        """מציאת פורטפוליוז עודפים"""
        
    def freeze():
        """נעילה במעבר ל-Step 3"""
        
    def unfreeze():
        """שחרור בחזרה ל-Step 2"""
```

#### 3. ניקוי ראשוני (Step 2)
```python
# core/validate/bulk_cleanse.py
def initial_cleanup(bulk_df, virtual_map) -> DataFrame:
    """
    ניקוי לפי האיפיון:
    1. Entity = "Keyword" או "Product Targeting"
    2. State = "enabled"
    3. Campaign State (Informational only) = "enabled"
    4. Ad Group State (Informational only) = "enabled"
    5. Portfolio Name קיים ב-Virtual Map
    """
```

#### 4. השוואת פורטפוליוז
```python
# core/validate/portfolios.py
def compare_portfolios(bulk_df, template_df) -> dict:
    """
    השוואה והחזרת:
    - missing: רשימת חסרים
    - excess: רשימת עודפים
    """
    
def create_completion_template(missing_portfolios) -> BytesIO:
    """יצירת טמפלט השלמה עם 3 עמודות"""
```

#### 5. יצירת קבצי Output
```python
# core/output/files_builder.py
def create_working_file(bulk_df, optimization_type="Zero Sales") -> BytesIO:
    """
    יצירת Working File:
    - לשונית "Clean Zero Sales" 
    - לשונית "Working Zero Sales"
    - Operation = "Update" בכל השורות
    """
    
def create_clean_file(bulk_df, optimization_type="Zero Sales") -> BytesIO:
    """
    יצירת Clean File:
    - רק לשונית "Clean Zero Sales"
    - Operation = "Update" בכל השורות
    """
    
def generate_filename(file_type) -> str:
    """
    פורמט: Auto Optimized Bulk | {type} | YYYY-MM-DD | HH-MM.xlsx
    """
```

---

## Phase 5: אינטגרציה וחיבור ⏳ טרם החל

### מה צריך לעשות:

1. **חיבור Step 1 (Upload) ללוגיקה**:
   - ולידציה אמיתית של headers
   - בדיקת גודל קובץ (40MB)
   - בדיקת קיום sheet "Sponsored Products Campaigns"

2. **חיבור Step 2 (Validate) ללוגיקה**:
   - **לשמור את Mockup Scenario Selector!**
   - הוספת לוגיקה אמיתית במקביל ל-Selector
   - ניקוי ראשוני אמיתי
   - Virtual Map פעיל
   - לולאת Completion Template

3. **חיבור Step 3 (Output) ללוגיקה**:
   - יצירת קבצים אמיתיים (זהים למקור)
   - שמות קבצים דינמיים
   - Operation = "Update" בכל השורות

---

## Phase 6: בדיקות וליטוש ⏳ טרם החל

### בדיקות נדרשות:
- [ ] העלאת קובץ 40MB
- [ ] העלאת קובץ עם headers שגויים
- [ ] לולאת Completion (3 איטרציות)
- [ ] תרחיש missing בלבד
- [ ] תרחיש excess בלבד
- [ ] תרחיש missing + excess
- [ ] כפתור Reset (New Processing)
- [ ] מעבר חלק בין טאבים
- [ ] **בדיקה עם Mockup Scenario Selector**

### ניקיון קוד:
- [ ] **לא להסיר את Mockup Scenario Selector** - זה נשאר!
- [ ] הסרת debug prints (אם יש)
- [ ] הסרת TODO comments
- [ ] וידוא שכל הטקסטים באנגלית
- [ ] וידוא שאין אימוג'י או אייקונים

---

## סדר עדיפויות מעודכן להמשך פיתוח

### עדיפות 1 - היסודות הקדושים
1. **`core/io/readers.py` ו-`writers.py`** - הלב הפועם של המוקאפ
2. **`core/mapping/virtual_map.py`** - המוח של המערכת
3. **`core/validate/bulk_cleanse.py`** - הניקוי הראשוני המיתולוגי

### עדיפות 2 - השלמת הזרימה
4. **`core/validate/portfolios.py`** - השוואת פורטפוליוז
5. **`core/output/files_builder.py`** - יצירת קבצי output
6. **חיבור הלוגיקה לטאבים** - אינטגרציה

### עדיפות 3 - ליטוש
7. **בדיקות מקיפות**
8. **תיעוד**

---

## הערות קריטיות

1. **זהו מוקאפ פונקציונלי, לא דמו** - הכל צריך לעבוד באמת
2. **Mockup Scenario Selector נשאר** - זה פיצ'ר חשוב לבדיקות
3. **Virtual Map הוא קריטי** - זה המנגנון המרכזי
4. **הסטיילינג קיים ומלא** - כפתורים אדומים, ללא אימוג'י, פריסה מדויקת
5. **יש קבצי דוגמה** - להשתמש בהם לבדיקות

---

## Timeline משוער

| Phase | זמן משוער | סטטוס | הערות |
|-------|----------|--------|--------|
| Phase 1 | הושלם | ✅ 100% | מבנה מלא |
| Phase 2 | הושלם | ✅ 90% | רק לוגיקת core חסרה |
| Phase 3 | הושלם | ✅ 75-80% | UI מלא, לוגיקה חסרה |
| Phase 4 | 2 ימים | ⏳ 0% | **עדיפות עליונה** |
| Phase 5 | 1 יום | ⏳ 0% | אינטגרציה |
| Phase 6 | 1 יום | ⏳ 0% | בדיקות |

**סה"כ זמן נותר: 4-5 ימים**

---

## הוראות מיוחדות למפתח

1. **התחל מ-Phase 4** - זה הכי קריטי
2. **אל תמחק את Mockup Scenario Selector**
3. **השתמש בקבצי הדוגמה לבדיקות**
4. **שמור על הסטיילינג הקיים**
5. **Virtual Map = קריטי להצלחה**

---

*מסמך זה מחליף את `PRD/development_plan.md` הקיים*