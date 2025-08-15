# פרק 1 - Virtual Map & Core Logic (יום 1 - 6 שעות)

## מטרה
לבנות את הלב של המערכת - הוירטואל מאפ שמנהל את כל הפורטפוליוז, ואת מנגנון ההשוואה שמזהה חסרים ועודפים. בלי זה שום דבר לא יעבוד.

## צקליסט בנייה

### משימה 1: core/mapping/virtual_map.py (120 דקות)

#### כתיבת הקוד
```python
- [ ] יצירת המחלקה VirtualMap
- [ ] __init__() - אתחול עם data={} ו-is_frozen=False
- [ ] add_portfolio(name, base_bid, target_cpa) - הוספת פורטפוליו
- [ ] remove_portfolio(name) - הסרת פורטפוליו (לאיגנור)
- [ ] freeze() - נעילה: self.is_frozen=True, self.frozen_copy=deepcopy(data)
- [ ] unfreeze() - ביטול נעילה (אם בכלל נדרש)
- [ ] is_frozen() - החזרת סטטוס
- [ ] get_frozen_copy() - החזרת העותק הקפוא
- [ ] merge_completion_template(df) - מיזוג קומפלישן עם דריסה
- [ ] get_data() - החזרת הדאטה (קפואה או רגילה)
```

#### בדיקות מפתח בקוד
```python
- [ ] def test_add_remove():
      vm = VirtualMap()
      vm.add_portfolio("Port_A", 1.5, 3.0)
      assert "Port_A" in vm.data
      vm.remove_portfolio("Port_A")
      assert "Port_A" not in vm.data
      
- [ ] def test_freeze_blocks_changes():
      vm = VirtualMap()
      vm.add_portfolio("Port_A", 1.5)
      vm.freeze()
      vm.add_portfolio("Port_B", 2.0)  # לא אמור להתווסף
      assert "Port_B" not in vm.data
      
- [ ] def test_merge_completion():
      vm = VirtualMap()
      df = pd.DataFrame({
          'Portfolio Name': ['Port_A'],
          'Base Bid': [1.5],
          'Target CPA': [3.0]
      })
      vm.merge_completion_template(df)
      assert vm.data['Port_A']['base_bid'] == 1.5
```

### משימה 2: core/validate/portfolio_comparison.py (90 דקות)

#### כתיבת הקוד
```python
- [ ] compare_portfolios(bulk_df, virtual_map) - השוואה ראשית
- [ ] get_missing_portfolios(bulk_list, vm_dict) - חסרים: בבאלק אבל לא בוירטואל מאפ
- [ ] get_excess_portfolios(bulk_list, vm_dict) - עודפים: בוירטואל מאפ אבל לא בבאלק
- [ ] extract_portfolio_names(df) - הוצאת שמות מדאטהפריים
- [ ] create_comparison_result(missing, excess) - יצירת תוצאה
```

#### בדיקות מפתח
```python
- [ ] def test_find_missing():
      bulk_portfolios = ["Port_A", "Port_B", "Port_C"]
      vm_portfolios = {"Port_A": {}}
      missing = get_missing_portfolios(bulk_portfolios, vm_portfolios)
      assert missing == ["Port_B", "Port_C"]
      
- [ ] def test_find_excess():
      bulk_portfolios = ["Port_A"]
      vm_portfolios = {"Port_A": {}, "Port_X": {}}
      excess = get_excess_portfolios(bulk_portfolios, vm_portfolios)
      assert excess == ["Port_X"]
```

### משימה 3: עדכון core/validate/bulk_cleanse.py (60 דקות)

#### עדכונים נדרשים
```python
- [ ] שיפור initial_cleanup() - להוסיף פילטר אנטיטי וסטייט
- [ ] filter_by_entity(df) - רק קיוורד או פרודקט טארגטינג
- [ ] filter_by_state(df) - כל 3 השדות חייבים להיות אינייבלד
- [ ] remove_ignored_portfolios(df, ignored_list) - הסרת איגנורד
- [ ] get_cleanup_statistics(before, after) - סטטיסטיקות
```

#### בדיקות מפתח
```python
- [ ] def test_entity_filter():
      df = pd.DataFrame({'Entity': ['Keyword', 'Campaign', 'Product Targeting']})
      filtered = filter_by_entity(df)
      assert len(filtered) == 2  # רק קיוורד ופרודקט
      
- [ ] def test_state_filter():
      df = pd.DataFrame({
          'State': ['enabled', 'paused'],
          'Campaign State (Informational only)': ['enabled', 'enabled']
      })
      filtered = filter_by_state(df)
      assert len(filtered) == 1  # רק הראשונה
```

## צקליסט בדיקות משתמש

### בדיקה 1: וירטואל מאפ בממשק
**מה לעשות:**
1. הרץ את האפליקציה
2. העלה טמפלייט עם 2 פורטפוליוז
3. עבור לטאב ולידייט
4. בדוק בקונסול (F12) אם יש שגיאות

**תוצאה צפויה:**
- הטאב נטען (אולי עם שגיאות)
- לא קורס לגמרי
- רואים התקדמות מהמצב הקודם

### בדיקה 2: השוואת פורטפוליוז
**מה לעשות:**
1. העלה טמפלייט עם 2 פורטפוליוז: Port_A, Port_B
2. העלה באלק עם 4 פורטפוליוז: Port_A, Port_B, Port_C, Port_D
3. עבור לולידייט

**תוצאה צפויה:**
- מופיעה הודעה על 2 חסרים
- מופיעים השמות: Port_C, Port_D
- יש כפתור להורדת קומפלישן טמפלייט

### בדיקה 3: סינון באלק
**מה לעשות:**
1. העלה באלק רגיל
2. עבור לולידייט
3. בדוק כמה שורות נשארו אחרי הניקוי

**תוצאה צפויה:**
- מספר השורות ירד משמעותית
- נשארו רק קיוורד ופרודקט טארגטינג
- נשארו רק אינייבלד

## צקליסט בדיקות מפתח

### בדיקה 1: וירטואל מאפ מלא
```python
# test_virtual_map_complete.py
def test_virtual_map_flow():
    """בדיקת זרימה מלאה של וירטואל מאפ"""
    from core.mapping.virtual_map import VirtualMap
    
    vm = VirtualMap()
    
    # הוספה
    vm.add_portfolio("Port_A", 1.5, 3.0)
    assert len(vm.data) == 1
    
    # קפיאה
    vm.freeze()
    assert vm.is_frozen() == True
    
    # ניסיון שינוי כשקפוא
    vm.add_portfolio("Port_B", 2.0)
    assert len(vm.data) == 1  # לא השתנה
    
    print("✓ Virtual Map works correctly")
```

**תוצאה צפויה:** כל הבדיקות עוברות

### בדיקה 2: השוואת פורטפוליוז
```python
# test_comparison.py
def test_portfolio_comparison():
    """בדיקת השוואת פורטפוליוז"""
    from core.validate.portfolio_comparison import get_missing_portfolios, get_excess_portfolios
    
    bulk = ["A", "B", "C", "D"]
    vm = {"A": {}, "B": {}, "X": {}}
    
    missing = get_missing_portfolios(bulk, vm)
    excess = get_excess_portfolios(bulk, vm)
    
    assert missing == ["C", "D"]
    assert excess == ["X"]
    
    print("✓ Comparison works correctly")
```

**תוצאה צפויה:** מזהה נכון חסרים ועודפים

### בדיקה 3: ניקוי באלק
```python
# test_bulk_cleanse.py
def test_bulk_cleaning():
    """בדיקת ניקוי באלק"""
    from core.validate.bulk_cleanse import filter_by_entity, filter_by_state
    import pandas as pd
    
    # בדיקת אנטיטי
    df = pd.DataFrame({
        'Entity': ['Keyword', 'Campaign', 'Product Targeting', 'Ad Group']
    })
    filtered = filter_by_entity(df)
    assert len(filtered) == 2
    
    print("✓ Bulk cleanse works")
```

**תוצאה צפויה:** מסנן נכון את הנתונים

## צקפוינט אמצע יום (3 שעות)
- [ ] VirtualMap מוכן עם freeze/unfreeze
- [ ] portfolio_comparison עובד
- [ ] 10+ טסטים עוברים

**אם נכשל:** התמקד רק בוירטואל מאפ, השאר ליום 2

## טיפול בבעיות נפוצות

### בעיה: ImportError עם VirtualMap
**פתרון:**
```python
# וודא שהפאת נכון
from core.mapping.virtual_map import VirtualMap
# לא from services או מקום אחר
```

### בעיה: freeze לא עובד
**פתרון:**
```python
# וודא שיש deepcopy
from copy import deepcopy
self.frozen_copy = deepcopy(self.data)
```

### בעיה: השוואה לא מוצאת חסרים
**פתרון:**
```python
# בדוק ששמות העמודות נכונים
'Portfolio Name (Informational only)'  # בבאלק
'Portfolio Name'  # בטמפלייט
```

## צקפוינט סוף יום
- [ ] VirtualMap - 7 פונקציות עובדות
- [ ] portfolio_comparison - 5 פונקציות עובדות
- [ ] bulk_cleanse - 5 פונקציות משופרות
- [ ] 20+ טסטים עוברים
- [ ] אפליקציה עדיין עולה
- [ ] טאב ולידייט מתחיל לעבוד

## סיכום הפרק
**השגנו:**
- הלב של המערכת עובד
- וירטואל מאפ מנהל נתונים
- השוואת פורטפוליוז פונקציונלית
- ניקוי באלק משופר

**מוכנים לפרק 2:**
- תשתית מוכנה לסטפ2 סרוויס
- יכולים לבנות את הלוגיקה העסקית
- הבסיס יציב

## חתימת סיום פרק 1
- [ ] תאריך: _______
- [ ] שעת התחלה: _______
- [ ] שעת סיום: _______
- [ ] שורות קוד: ~400
- [ ] טסטים עוברים: ___ / 20
- [ ] הערות: _______