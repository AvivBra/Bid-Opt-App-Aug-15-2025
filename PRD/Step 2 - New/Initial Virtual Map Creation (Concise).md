# יצירת Virtual Map ראשוני - מפרט תמציתי

## מטרה
יצירת מבנה נתונים מ-Template File לניהול פורטפוליוז.

## קלט
Template File עם 3 עמודות:
- Portfolio Name
- Base Bid  
- Target CPA

## לוגיקת עיבוד

| Base Bid | פעולה |
|----------|--------|
| "Ignore" | הוסף לרשימת ignored_portfolios |
| מספר תקין (≥0) | הוסף ל-Virtual Map |
| לא תקין | דלג בשקט |

## פלט

### 1. Virtual Map
```python
{
    "portfolio_name": {
        "base_bid": float,
        "target_cpa": float | None
    }
}
```

### 2. Ignored List
```python
["Portfolio_A", "Portfolio_B"]
```

## דוגמה

| Portfolio | Base Bid | Target CPA | תוצאה |
|-----------|----------|------------|--------|
| Port_A | 1.5 | 3.0 | → Virtual Map |
| Port_B | Ignore | | → Ignored List |
| Port_C | xyz | | → נדלג |
| Port_D | -2 | | → נדלג |

## הערות
- התהליך מתבצע פעם אחת בכניסה ל-Step 2
- אין הודעות שגיאה על שורות שנדלגו
- פורטפוליוז שנדלגו יזוהו כ"חסרים" בהשוואה