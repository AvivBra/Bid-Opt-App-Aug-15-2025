# Test Scenarios - Bid Optimizer

## תרחיש 1: Happy Path - הכל עובד מושלם ✅

### תיאור
משתמש עם קבצים תקינים שרוצה להריץ אופטימיזציה אחת

### צעדים
1. **פתח אפליקציה**
   - רואה: Upload section, כפתור Download Template

2. **הורד והכן Template**
   - לחץ: Download Template
   - מלא: 3 פורטפוליוז עם Base Bid
   - שמור: template.xlsx

3. **העלה קבצים**
   - העלה: template.xlsx (125KB)
   - העלה: bulk.xlsx (2.3MB) 
   - רואה: ✓ על שני הקבצים

4. **בחר אופטימיזציה**
   - סמן: Zero Sales
   - רואה: ☑ Zero Sales

5. **ולידציה**
   - רואה: "✓ All portfolios valid"
   - כפתור Process Files פעיל

6. **עיבוד**
   - לחץ: Process Files
   - רואה: Progress bar
   - רואה: "✓ Processing complete"

7. **הורדה**
   - לחץ: Download Working File
   - לחץ: Download Clean File
   - בדוק: קבצים נפתחים ב-Excel

### תוצאה צפויה
- 2 קבצים הורדו בהצלחה
- שמות: "Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx"
- Working: 2 sheets, Clean: 1 sheet

---

## תרחיש 2: Missing Portfolios - תיקון בעיה 🔧

### תיאור
Template חסרים בו 2 פורטפוליוז שקיימים ב-Bulk

### צעדים
1. **העלה קבצים**
   - template_partial.xlsx (רק 3 מתוך 5 פורטפוליוז)
   - bulk_complete.xlsx (5 פורטפוליוז)

2. **ראה שגיאה**
   - רואה: "❌ Missing portfolios found"
   - רואה: "Missing: Portfolio_D, Portfolio_E"
   - כפתור: "Upload New Template" (אדום)

3. **תקן את הבעיה**
   - הכן: template_fixed.xlsx עם כל 5 הפורטפוליוז
   - לחץ: Upload New Template
   - העלה: template_fixed.xlsx

4. **ולידציה חוזרת**
   - רואה: "✓ All portfolios valid"
   - כפתור Process Files פעיל

5. **המשך רגיל**
   - Process → Download → Success

### תוצאה צפויה
- שגיאה מזוהה ומוסברת בבירור
- ניתן לתקן בלי לאבד את ה-Bulk
- אחרי תיקון הכל עובד

---

## תרחיש 3: File Too Large - קובץ גדול מדי ⚠️

### תיאור
משתמש מנסה להעלות Bulk של 41MB

### צעדים
1. **העלה Template תקין**
   - template.xlsx מועלה בהצלחה

2. **נסה להעלות Bulk גדול**
   - בחר: huge_bulk.xlsx (41MB)
   - רואה מיד: "❌ File exceeds 40MB limit"

3. **הקובץ לא נטען**
   - Bulk status: "✗ Not uploaded"
   - אין Progress bar שנתקע

4. **העלה קובץ קטן יותר**
   - bulk_smaller.xlsx (35MB)
   - רואה: "✓ Bulk uploaded"

5. **המשך רגיל**
   - Validation → Process → Download

### תוצאה צפויה
- שגיאה מיידית (לא מחכים לטעינה)
- הודעה ברורה על המגבלה
- ניתן להעלות קובץ אחר

---

## תרחיש 4: Multiple Optimizations - 5 אופטימיזציות ⚡

### תיאור
משתמש רוצה להריץ 5 אופטימיזציות במקביל

### צעדים
1. **העלה קבצים תקינים**
   - template.xlsx ✓
   - bulk.xlsx ✓

2. **בחר 5 אופטימיזציות**
   - ☑ Zero Sales
   - ☑ Portfolio Bid
   - ☑ Budget Optimization
   - ☑ Keyword Optimization
   - ☑ ASIN Targeting

3. **עיבוד**
   - לחץ: Process Files
   - רואה: Progress bar (אולי יותר איטי)
   - רואה: "Processing Portfolio Bid..."

4. **בדוק תוצאות**
   - Working File: 10 sheets (5x2)
   - Clean File: 5 sheets
   - Pink notice: "Please note: 12 calculation errors"

5. **הורד ובדוק**
   - פתח Working File
   - ראה 10 sheets עם שמות נכונים
   - כל sheet עם Operation="Update"

### תוצאה צפויה
- כל האופטימיזציות רצות
- קובץ גדול יותר אבל מאורגן
- הודעה על שגיאות חישוב

---

## תרחיש 5: Reset Flow - התחלה מחדש 🔄

### תיאור
משתמש רוצה להתחיל מחדש עם קבצים אחרים

### צעדים
1. **השלם תהליך מלא**
   - Upload → Validate → Process → Download

2. **לחץ Reset**
   - לחץ: כפתור Reset (אפור)
   - רואה: חזרה למסך התחלתי

3. **בדוק שהכל נוקה**
   - Template: "✗ Not uploaded"
   - Bulk: "✗ Not uploaded"
   - Checkboxes: לא מסומנים (חוץ מ-Zero Sales)
   - Validation section: מוסתר
   - Output section: מוסתר

4. **התחל תהליך חדש**
   - העלה קבצים חדשים
   - עובד כרגיל

### תוצאה צפויה
- ניקוי מלא של המערכת
- אין "זכרונות" מהריצה הקודמת
- מוכן לתהליך חדש

---

## סיכום בדיקות קריטיות

| תרחיש | מה נבדק | Pass Criteria |
|-------|----------|---------------|
| Happy Path | התהליך המלא | קבצים מורדים תקינים |
| Missing Portfolios | טיפול בשגיאות | ניתן לתקן ולהמשיך |
| File Too Large | מגבלות גודל | דחייה מיידית + הודעה |
| Multiple Optimizations | עומס | כל האופטימיזציות רצות |
| Reset | ניקוי | התחלה נקייה |

## בדיקות מהירות לפני Release

1. ✅ Template ריק מוריד
2. ✅ קבצים נטענים
3. ✅ ולידציה עובדת
4. ✅ Process יוצר קבצים
5. ✅ Download עובד
6. ✅ Reset מנקה
7. ✅ שגיאות מוצגות נכון
8. ✅ Progress bar זז