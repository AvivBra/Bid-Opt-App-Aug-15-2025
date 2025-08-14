# מבנה Virtual Map - מפרט טכני

## מטרה
Virtual Map הוא מבנה הנתונים המרכזי שמנהל את כל נתוני הפורטפוליוז לאורך Step 2.

## מבנה הנתונים

### מבנה ראשי
```python
class VirtualMap:
    data: Dict[str, dict]           # פורטפוליוז פעילים
    ignored_portfolios: List[str]   # פורטפוליוז מסומנים להתעלמות
    is_frozen: bool                  # האם נעול
    frozen_copy: dict               # עותק קפוא לStep 3
```

### מבנה Portfolio Entry
```python
{
    "portfolio_name": {
        "base_bid": float,          # ערך הבייס ביד
        "target_cpa": float | None  # ערך הטארגט (אופציונלי)
    }
}
```

## פונקציות עיקריות

| פונקציה | תיאור | קלט | פלט |
|----------|--------|------|------|
| `add_portfolio()` | הוספת פורטפוליו | name, base_bid, target_cpa | - |
| `add_ignored()` | הוספה לרשימת ignored | name | - |
| `remove_portfolio()` | מחיקת פורטפוליו | name | - |
| `get_missing_portfolios()` | מציאת חסרים | bulk_portfolios list | missing list |
| `get_excess_portfolios()` | מציאת עודפים | bulk_portfolios list | excess list |
| `merge_completion_template()` | מיזוג נתונים | completion_df, bulk_portfolios | errors dict |
| `freeze()` | נעילה לStep 3 | - | - |
| `get_data()` | קבלת הנתונים | - | data dict |
| `get_ignored()` | קבלת רשימת ignored | - | ignored list |

## מצבי Virtual Map

### מצב Active (Step 2)
- ניתן לעדכון ושינוי
- מקבל נתונים חדשים
- מאפשר מיזוגים

### מצב Frozen (Step 3)
- Read-only
- לא ניתן לשינוי
- משמש לחישובים בלבד

## כללי ניהול

### הוספת פורטפוליו
- Base Bid חייב להיות מספר תקין (≥0)
- Target CPA אופציונלי
- אם קיים - דורס את הקיים

### סימון כ-Ignore
- הפורטפוליו נמחק מ-data
- נוסף ל-ignored_portfolios
- כל השורות שלו יסוננו מה-Bulk

### חישוב חסרים
```
חסרים = פורטפוליוז בבלק - פורטפוליוז בוירטואל מאפ - פורטפוליוז באיגנור
```

### חישוב עודפים
```
עודפים = פורטפוליוז בוירטואל מאפ - פורטפוליוז בבלק
```

## דוגמה מלאה

### מצב התחלתי (אחרי טמפלט):
```python
VirtualMap:
  data: {
    "Port_A": {"base_bid": 1.5, "target_cpa": 3.0},
    "Port_B": {"base_bid": 2.0, "target_cpa": None}
  }
  ignored_portfolios: ["Port_X", "Port_Y"]
```

### אחרי Completion Template:
```python
VirtualMap:
  data: {
    "Port_A": {"base_bid": 2.5, "target_cpa": 4.0},  # דרוס
    "Port_B": {"base_bid": 2.0, "target_cpa": None},  # ללא שינוי
    "Port_C": {"base_bid": 1.0, "target_cpa": None}   # חדש
  }
  ignored_portfolios: ["Port_X", "Port_Y", "Port_D"]  # Port_D נוסף
```

## הערות
- Virtual Map הוא המקור היחיד לאמת לגבי פורטפוליוז
- לאחר הקפאה בסוף Step 2 - לא ניתן לשינוי
- הנתונים עוברים ל-Step 3 בצורה קפואה