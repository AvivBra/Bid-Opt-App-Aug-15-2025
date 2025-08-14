# Step 2 - Examples and Scenarios

## תרחיש 1: אין חסרים או עודפים

### תרשים זרימה
```
[START]
    ↓
[Template: Port_A, Port_B]
    ↓
[Bulk (אחרי ניקוי): Port_A, Port_B]
    ↓
[השוואה: 0 חסרים, 0 עודפים]
    ↓
[הקפאת Virtual Map]
    ↓
[טריגור Step 3]
```

### דוגמה
- **Template**: Port_A (bid=1.5), Port_B (bid=2.0)
- **Bulk**: Port_A, Port_B
- **תוצאה**: מעבר ישיר ל-Step 3

---

## תרחיש 2: חסרים בלבד

### תרשים זרימה
```
[START]
    ↓
[Template: Port_A]
    ↓
[Bulk: Port_A, Port_B, Port_C]
    ↓
[השוואה: 2 חסרים (B,C), 0 עודפים]
    ↓
[יצירת Completion Template]
    ↓
[משתמש ממלא וטוען]
    ↓
[מיזוג ל-Virtual Map]
    ↓
[ניקוי מחדש + השוואה]
    ↓
[0 חסרים → הקפאה → Step 3]
```

### דוגמה עם 2 איטרציות
**איטרציה 1:**
- חסרים: Port_B, Port_C
- משתמש ממלא: Port_B (bid=1.0), Port_C (שגיאה - ריק)
- תוצאה: Port_C עדיין חסר

**איטרציה 2:**
- חסר: Port_C
- משתמש ממלא: Port_C (bid=1.5)
- תוצאה: אין חסרים → Step 3

---

## תרחיש 3: עודפים בלבד

### תרשים זרימה
```
[START]
    ↓
[Template: Port_A, Port_B, Port_X, Port_Y]
    ↓
[Bulk: Port_A, Port_B]
    ↓
[השוואה: 0 חסרים, 2 עודפים (X,Y)]
    ↓
[הצגת רשימת עודפים]
    ↓
[כפתור Copy to Clipboard]
    ↓
[כפתור Continue מופעל]
    ↓
[הקפאה → Step 3]
```

### דוגמה
- **Template**: Port_A, Port_B, Port_X, Port_Y
- **Bulk**: Port_A, Port_B בלבד
- **עודפים**: Port_X, Port_Y
- **פעולה**: משתמש מעתיק רשימה ולוחץ Continue

---

## תרחיש 4: חסרים ועודפים

### תרשים זרימה
```
[START]
    ↓
[Template: Port_A, Port_X]
    ↓
[Bulk: Port_A, Port_B, Port_C]
    ↓
[השוואה: 2 חסרים (B,C), 1 עודף (X)]
    ↓
[הצגת עודפים + לולאת חסרים]
    ↓
[Completion Template למילוי]
    ↓
[משתמש ממלא]
    ↓
[מיזוג + ניקוי + השוואה]
    ↓
[0 חסרים, 1 עודף]
    ↓
[Continue מופעל → Step 3]
```

### דוגמה מלאה - 3 איטרציות

#### מצב התחלתי
- **Template**: Port_A (bid=1.5), Port_X (bid=3.0)
- **Bulk**: Port_A, Port_B, Port_C, Port_D
- **השוואה**: חסרים=[B,C,D], עודפים=[X]

#### איטרציה 1
- **Completion Template**: Port_B, Port_C, Port_D
- **משתמש ממלא**: 
  - Port_B (bid=2.0)
  - Port_C (Ignore)
  - Port_D (ריק - שגיאה)
- **תוצאה**: Port_D עדיין חסר

#### איטרציה 2
- **Bulk אחרי ניקוי**: Port_A, Port_B, Port_D (Port_C נעלם)
- **Completion Template**: Port_D + הודעת שגיאה
- **משתמש ממלא**: Port_D (bid=1.8)
- **תוצאה**: אין חסרים

#### איטרציה 3
- **בדיקה סופית**: 0 חסרים, 1 עודף (Port_X)
- **תוצאה**: Continue → Step 3

---

## תרחיש 5: Ignore בטמפלט המקורי

### דוגמה
- **Template מקורי**: 
  - Port_A (bid=1.5)
  - Port_B (Ignore)
  - Port_C (bid=2.0)
- **Bulk**: Port_A, Port_B, Port_C, Port_D
- **Virtual Map נוצר**: {Port_A: 1.5, Port_C: 2.0}
- **Ignored list**: [Port_B]
- **Bulk אחרי ניקוי**: Port_A, Port_C, Port_D (Port_B נעלם)
- **חסרים**: Port_D בלבד

---

## תרחיש 6: טיפול בשגיאות

### דוגמת שגיאות ב-Completion Template
1. **Base Bid ריק**: חזרה למילוי עם הודעה
2. **Base Bid לא תקין** (טקסט): חזרה למילוי עם הודעה
3. **Portfolio לא קיים בבאלק**: הודעת שגיאה ספציפית
4. **Target CPA שגוי**: חזרה למילוי עם הודעה

### תרשים טיפול בשגיאות
```
[העלאת Completion Template]
    ↓
[ולידציה]
    ├─[תקין] → [מיזוג]
    └─[שגיאות] → [יצירת Template חדש עם עמודת Error]
                    ↓
                  [הודעה S2-007]
                    ↓
                  [חזרה להורדה]
```