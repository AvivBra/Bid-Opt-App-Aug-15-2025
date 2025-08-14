# Step 2 - Documentation and Code References

## טבלת מסמכי איפיון

| שלב | מסמך איפיון | תיאור | סטטוס |
|-----|-------------|-------|--------|
| 1 | Initial Virtual Map Creation (Concise).md | יצירת Virtual Map מהטמפלט הראשוני | ✓ |
| 2 | Initial Bulk Cleanup (Concise).md | ניקוי וסינון שורות לא רלוונטיות | ✓ מתוקן |
| 3 | Master Process Flow.md | תהליך כללי והשוואת פורטפוליוז | ✓ |
| 4 | Completion Template Merge (Concise).md | מיזוג נתונים מ-Completion Template | ✓ |
| 5 | Virtual Map Freeze (Concise).md | נעילת הנתונים לפני Step 3 | ✓ |
| - | Virtual Map Structure.md | מבנה נתונים של Virtual Map | ✓ |
| - | Step 2 - Examples and Scenarios.md | דוגמאות ותרחישים | ✓ |
| - | Errors.md | הודעות שגיאה S2-xxx | ✓ |


## מבנה Virtual Map - סיכום

### Class Structure
```python
class VirtualMap:
    data: Dict[str, dict]           # פורטפוליוז פעילים
    ignored_portfolios: List[str]   # רשימת ignored
    is_frozen: bool                  # סטטוס נעילה
    frozen_copy: dict               # עותק קפוא
```

### Portfolio Entry
```python
{
    "portfolio_name": {
        "base_bid": float,
        "target_cpa": float | None
    }
}
```

## זרימת נתונים בין הקבצים

```
Template File → initialize_virtual_map() → Virtual Map
                                              ↓
Bulk File → initial_cleanup(ignored_list) → Cleaned Bulk
                                              ↓
                    get_missing_portfolios() → Missing List
                                              ↓
                    create_completion_template() → Excel File
                                              ↓
User Input → merge_completion_template() → Updated Virtual Map
                                              ↓
                            freeze() → Frozen Virtual Map → Step 3
```

## הערות חשובות לפיתוח

1. **שמות שדות מדויקים**: 
   - בבאלק: "Portfolio Name (Informational only)"
   - בטמפלט: "Portfolio Name"

2. **מעגליות התהליך**: 
   - כל מיזוג → ניקוי מחדש → השוואה מחדש

3. **איפוס בשינוי Step 1**: 
   - העלאת קובץ חדש ב-Step 1 מאפסת הכל

4. **חד-כיווניות**: 
   - אחרי הקפאה אין חזרה (רק New Processing)