# מיזוג Completion Template - מפרט תמציתי

## מטרה
עדכון Virtual Map עם נתונים מ-Completion Template להשלמת פורטפוליוז חסרים.

## קלט
Completion Template שהמשתמש מילא (Portfolio Name, Base Bid, Target CPA)

## לוגיקת מיזוג

| Base Bid | פעולה | **ולידציה** |
|----------|--------|----------|
| "Ignore" | מחק מ-Virtual Map + הוסף ל-ignored list | - |
| מספר תקין (≥0) | דרוס/הוסף ל-Virtual Map (דריסה מלאה) | **בדוק שהפורטפוליו קיים ב-Bulk** |
| לא תקין | **דחה את כל הקובץ** + הודעת שגיאה | - |

## תוצאה סופית
Virtual Map שכולל:
- כל הפורטפוליוז התקינים מה-Template המקורי
- **פלוס** כל הפורטפוליוז התקינים מ-Completion Template
- **מינוס** פורטפוליוז שסומנו כ-Ignore

פורטפוליוז עם שגיאות חוזרים לקומפלישן טמפלט הבא להשלמה

## ולידציות וטיפול בשגיאות
- Base Bid ריק או לא תקין → הוספה לקומפלישן טמפלט הבא עם הערה
- Portfolio לא קיים ב-Bulk המנוקה → הוספה לקומפלישן טמפלט הבא עם הערה
- Target CPA לא תקין → הוספה לקומפלישן טמפלט הבא עם הערה
- הודעה כללית למשתמש: "Missing or invalid values found. Please download template, fill and upload again"
- עמודה רביעית "Error" בקומפלישן טמפלט עם: "Invalid value, please correct"

## דוגמה

### לפני:
```python
Virtual Map: {"A": {base_bid: 1.5, target_cpa: 3.0}}
Ignored: []
```

### Completion Template:
| Portfolio | Base Bid | Target CPA |
|-----------|----------|------------|
| A | 2.0 | 4.0 |
| B | 1.0 | |
| C | Ignore | |

### אחרי:
```python
Virtual Map: {
    "A": {base_bid: 2.0, target_cpa: 4.0},  # דרוס
    "B": {base_bid: 1.0, target_cpa: None}   # חדש
}
Ignored: ["C"]
```

## הערות
- **דריסה מלאה** - אין מיזוג חלקי של ערכים
- התהליך חוזר בלולאה עד שאין חסרים
- כל העלאה דורסת את קודמתה
- **מיזוגים אפשריים רק ב-Step 2** - לאחר הקפאה אין אפשרות לשנות