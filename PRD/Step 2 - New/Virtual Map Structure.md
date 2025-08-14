# מבנה Virtual Map - מפרט טכני

## מטרה
Virtual Map הוא מבנה הנתונים המרכזי שמנהל את כל נתוני הפורטפוליוז לאורך Step 2.
התפקיד של המפה הוירטואלית הוא לשמור רישום של הפורטפוליוז התקינים שיש לנו מידע עליהם כדי שנדע על אילו פורטפפוליוז עדיין חסר מידע, ונדע האם צריך להמשיך בלופ השלמת המידע

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

### פונקציות בנייה ועדכון
- **`add_portfolio(name, base_bid, target_cpa)`** - הוספת פורטפוליו חדש או עדכון קיים
- **`add_ignored(name)`** - הוספה לרשימת ignored והסרה מ-data
- **`remove_portfolio(name)`** - מחיקת פורטפוליו (משמש כש-Base Bid="Ignore")

### פונקציות השוואה
- **`get_missing_portfolios(bulk_portfolios)`** - מחזיר רשימת פורטפוליוז חסרים (בבאלק אך לא ב-VM)
- **`get_excess_portfolios(bulk_portfolios)`** - מחזיר רשימת פורטפוליוז עודפים (ב-VM אך לא בבאלק)

### פונקציות מיזוג
- **`merge_completion_template(completion_df, bulk_portfolios)`** - מיזוג נתונים מ-Completion Template עם דריסה מלאה, מחזיר dictionary של שגיאות

### פונקציות מצב
- **`freeze()`** - נעילה חד-פעמית במעבר ל-Step 3, יוצר עותק קפוא
- **`unfreeze()`** - **לא בשימוש!** קיים טכנית אבל לא מופעל (אין חזרה מ-frozen)
- **`get_data()`** - מחזיר את הנתונים (frozen copy אם נעול, אחרת data רגיל)
- **`get_ignored()`** - מחזיר רשימת הפורטפוליוז ב-ignored

### פונקציות עזר
- **`is_empty()`** - בדיקה האם ה-Virtual Map ריק
- **`clear()`** - **לא בשימוש במהלך Step 2!** משמש רק באיפוס מלא של המערכת (`SessionManager.reset_for_new_processing()`)

## הערות חשובות על השימוש
- Virtual Map **לא מתרוקן** במהלך Step 2 - רק נבנה, מתמלא וננעל
- פונקציית `clear()` קיימת רק לצורך איפוס מלא בין הרצות
- פונקציית `unfreeze()` קיימת בקוד אך **לא נקראת** - אין חזרה מ-frozen
- זרימת המצבים: ריק → מתמלא (לולאה) → נעול → איפוס מלא (חוזר לריק)


## מצבי Virtual Map

### מצב Active (Step 2)
- ניתן לעדכון ושינוי
- מקבל נתונים חדשים
- מאפשר מיזוגים

### מצב Frozen (Step 3)
- Read-only
- לא ניתן לשינוי
- משמש לחישובים בלבד

### כללי מעבר בין מצבים
- **Active → Frozen**: חד-פעמי, בסיום Step 2
- **Frozen → Active**: אין! רק דרך איפוס מלא
- **ניווט לא משנה מצב**: מעבר בין טאבים לא משפיע על המצב

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