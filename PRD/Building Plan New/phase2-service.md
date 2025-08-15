# פרק 2 - Step2Service & Integration (יום 2 - 6 שעות)

## מטרה
לבנות את הלוגיקה העסקית המרכזית שמתזמרת את כל סטפ 2. הסרוויס ינהל את הוירטואל מאפ, יטפל בלולאת הקומפלישן, יספור איטרציות וימנע לולאות אינסופיות.

## צקליסט בנייה

### משימה 1: services/step2_service.py (150 דקות)

#### כתיבת הקוד
```python
- [ ] class Step2Service - הגדרת המחלקה
- [ ] __init__(self) - אתחול עם iteration_count=0
- [ ] MAX_ITERATIONS = 10 - קבוע למגבלה
- [ ] process_validation(bulk_df, template_df) - תזמור ראשי
- [ ] initialize_virtual_map(template_df) - אתחול וירטואל מאפ מטמפלייט
- [ ] handle_bulk_cleanse(bulk_df, ignored_list) - ניקוי באלק
- [ ] compare_portfolios(cleaned_bulk, virtual_map) - השוואה
- [ ] handle_missing_portfolios(missing_list) - יצירת קומפלישן טמפלייט
- [ ] merge_completion(completion_df) - מיזוג תוצאות
- [ ] check_iteration_limit() - בדיקת מגבלה
- [ ] increment_iteration() - הגדלת מונה עם בדיקה
- [ ] freeze_virtual_map() - נעילה בסוף התהליך
```

#### בדיקות מפתח
```python
- [ ] def test_initialization():
      s2 = Step2Service()
      assert s2.iteration_count == 0
      assert s2.MAX_ITERATIONS == 10
      
- [ ] def test_iteration_limit():
      s2 = Step2Service()
      for i in range(9):
          s2.increment_iteration()
      assert s2.iteration_count == 9
      # הבאה צריכה לזרוק שגיאה
      with pytest.raises(Exception):
          s2.increment_iteration()
          
- [ ] def test_full_flow():
      s2 = Step2Service()
      result = s2.process_validation(test_bulk, test_template)
      assert result is not None
      assert hasattr(result, 'missing')
      assert hasattr(result, 'excess')
```

### משימה 2: app/state/session.py - עדכון (30 דקות)

#### עדכונים נדרשים
```python
- [ ] הוספת completion_iteration_count = 0
- [ ] הוספת MAX_ITERATIONS = 10
- [ ] increment_iteration_counter() - הגדלת מונה
- [ ] reset_iteration_counter() - איפוס
- [ ] get_iteration_display() - החזרת "Attempt X/10"
```

#### בדיקות מפתח
```python
- [ ] def test_session_iteration():
      import streamlit as st
      from app.state.session import increment_iteration_counter
      
      st.session_state.completion_iteration_count = 0
      increment_iteration_counter()
      assert st.session_state.completion_iteration_count == 1
```

### משימה 3: core/validate/completion_validator.py (90 דקות)

#### כתיבת הקוד
```python
- [ ] validate_completion_template(df, bulk_portfolios) - ולידציה ראשית
- [ ] check_required_columns(df) - בדיקת עמודות
- [ ] check_base_bid_values(df) - בדיקת ערכי בייס ביד
- [ ] check_portfolio_exists(name, bulk_list) - בדיקה שפורטפוליו קיים
- [ ] check_all_ignored(df) - בדיקה שלא כולם איגנור
- [ ] create_validation_errors(df) - יצירת רשימת שגיאות
```

#### בדיקות מפתח
```python
- [ ] def test_valid_template():
      df = pd.DataFrame({
          'Portfolio Name': ['Port_A'],
          'Base Bid': [1.5],
          'Target CPA': [3.0]
      })
      errors = validate_completion_template(df, ['Port_A'])
      assert len(errors) == 0
      
- [ ] def test_invalid_base_bid():
      df = pd.DataFrame({
          'Portfolio Name': ['Port_A'],
          'Base Bid': ['invalid']
      })
      errors = check_base_bid_values(df)
      assert len(errors) > 0
      
- [ ] def test_all_ignored_error():
      df = pd.DataFrame({
          'Portfolio Name': ['A', 'B'],
          'Base Bid': ['Ignore', 'Ignore']
      })
      assert check_all_ignored(df) == True
```

### משימה 4: models/step2_models.py (60 דקות)

#### כתיבת הקוד
```python
- [ ] @dataclass ComparisonResult
      missing: List[str]
      excess: List[str]
      iteration: int
      can_proceed: bool
      
- [ ] @dataclass ValidationError
      portfolio: str
      field: str
      message: str
      
- [ ] @dataclass Step2State
      virtual_map: dict
      iteration_count: int
      is_frozen: bool
```

## צקליסט בדיקות משתמש

### בדיקה 1: לולאת קומפלישן
**מה לעשות:**
1. העלה טמפלייט עם 1 פורטפוליו
2. העלה באלק עם 3 פורטפוליוז
3. עבור לולידייט
4. הורד קומפלישן טמפלייט
5. מלא רק 1 פורטפוליו
6. העלה חזרה

**תוצאה צפויה:**
- מופיע "Attempt 1/10"
- אחרי העלאה - מופיע "1 missing portfolio"
- מופיע "Attempt 2/10"
- הלולאה ממשיכה

### בדיקה 2: מגבלת איטרציות
**מה לעשות:**
1. המשך את הלולאה מבדיקה 1
2. חזור על העלאה חלקית 10 פעמים

**תוצאה צפויה:**
- אחרי 10 פעמים - הודעת שגיאה
- "Maximum iterations (10) reached"
- לא ניתן להמשיך

### בדיקה 3: כולם איגנור
**מה לעשות:**
1. הורד קומפלישן טמפלייט
2. כתוב "Ignore" בכל השורות
3. העלה

**תוצאה צפויה:**
- הודעת שגיאה אדומה
- "All portfolios marked as Ignore"
- לא ניתן להמשיך

## צקליסט בדיקות מפתח

### בדיקה 1: סרוויס אינטגרציה
```python
# test_step2_service_integration.py
def test_service_with_real_data():
    """בדיקת סרוויס עם נתונים אמיתיים"""
    from services.step2_service import Step2Service
    import pandas as pd
    
    s2 = Step2Service()
    
    # טעינת קבצי דוגמה
    bulk = pd.read_excel('Bulk File Example.xlsx')
    template = pd.read_excel('Empty Template Example.xlsx')
    
    # הרצה
    result = s2.process_validation(bulk, template)
    
    assert result is not None
    assert isinstance(result.missing, list)
    assert s2.iteration_count == 0  # עדיין לא היו איטרציות
    
    print("✓ Service works with real files")
```

**תוצאה צפויה:** הסרוויס עובד עם קבצים אמיתיים

### בדיקה 2: מונה איטרציות
```python
# test_iteration_counter.py
def test_iteration_management():
    """בדיקת ניהול איטרציות"""
    from services.step2_service import Step2Service
    
    s2 = Step2Service()
    
    # בדיקת תקינות
    for i in range(9):
        s2.increment_iteration()
        assert s2.iteration_count == i + 1
    
    # בדיקת מגבלה
    try:
        s2.increment_iteration()  # ה-10
        s2.increment_iteration()  # ה-11 - צריך להיכשל
        assert False, "Should have raised error"
    except Exception as e:
        assert "Maximum iterations" in str(e)
    
    print("✓ Iteration limit enforced")
```

**תוצאה צפויה:** מגבלת 10 איטרציות נאכפת

### בדיקה 3: ולידציית קומפלישן
```python
# test_completion_validation.py
def test_completion_validator():
    """בדיקת ולידציית קומפלישן"""
    from core.validate.completion_validator import validate_completion_template
    import pandas as pd
    
    # תקין
    valid_df = pd.DataFrame({
        'Portfolio Name': ['Port_A'],
        'Base Bid': [1.5],
        'Target CPA': [None]
    })
    errors = validate_completion_template(valid_df, ['Port_A'])
    assert len(errors) == 0
    
    # שגוי
    invalid_df = pd.DataFrame({
        'Portfolio Name': ['Port_X'],  # לא קיים
        'Base Bid': ['abc']  # לא מספר
    })
    errors = validate_completion_template(invalid_df, ['Port_A'])
    assert len(errors) > 0
    
    print("✓ Validator catches errors")
```

**תוצאה צפויה:** הולידטור תופס שגיאות

## צקפוינט אמצע יום (3 שעות)
- [ ] Step2Service עובד
- [ ] מונה איטרציות פעיל
- [ ] ולידטור תופס שגיאות
- [ ] 15+ טסטים עוברים

**אם נכשל:** התמקד בסרוויס בלבד, ולידטור ליום 3

## טיפול בבעיות נפוצות

### בעיה: Circular import עם VirtualMap
**פתרון:**
```python
# בתוך הפונקציה, לא בראש הקובץ
def process_validation():
    from core.mapping.virtual_map import VirtualMap
    vm = VirtualMap()
```

### בעיה: סשן סטייט לא נשמר
**פתרון:**
```python
# וודא שמשתמש בסשן סטייט של סטרימליט
import streamlit as st
if 'iteration_count' not in st.session_state:
    st.session_state.iteration_count = 0
```

### בעיה: איטרציות לא נספרות
**פתרון:**
```python
# וודא שקורא לפונקציה הנכונה
self.increment_iteration()  # לא רק self.iteration_count += 1
```

## צקפוינט סוף יום
- [ ] Step2Service - 12 פונקציות עובדות
- [ ] session.py - מונה איטרציות עובד
- [ ] completion_validator - 6 פונקציות עובדות
- [ ] step2_models - 3 דאטהקלאסים
- [ ] 30+ טסטים עוברים
- [ ] לולאת קומפלישן עובדת

## סיכום הפרק
**השגנו:**
- לוגיקה עסקית מרכזית עובדת
- מנגנון איטרציות עם מגבלה
- ולידציה מלאה לקומפלישן
- תזמור כל סטפ 2

**מוכנים לפרק 3:**
- הלוגיקה קיימת בסרוויס
- אפשר להפריד מהיו-איי
- הבסיס יציב לריפקטור

## חתימת סיום פרק 2
- [ ] תאריך: _______
- [ ] שעת התחלה: _______
- [ ] שעת סיום: _______
- [ ] שורות קוד: ~500
- [ ] טסטים עוברים: ___ / 30
- [ ] הערות: _______