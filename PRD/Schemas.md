# PRD – סכמות קבצים (Template, Clean, Working)

## 1. מבוא
מסמך זה מגדיר את מבנה העמודות (Schema) והפורמט של קובצי הקלט והפלט במערכת **Bid & Budget Optimizer**.  
בשלב זה האפיון מתייחס ל־Template ולגרסת המוקאפ של קבצי הפלט (Clean ו־Working).

---

## 2. Template File – סכמת עמודות

| עמודה | סוג נתון | חובת מילוי | ערכים מותרים | הערות |
|-------|----------|------------|--------------|-------|
| **Portfolio Name** | טקסט | חובה | כל מחרוזת טקסט | שם הפורטפוליו כפי שמופיע ב־Bulk File |
| **Base Bid** | מספר או טקסט | חובה | מספר עשרוני חיובי עד 3 ספרות אחרי הנקודה, או `"Ignore"` | אם הערך הוא `"Ignore"` – המערכת תדלג על הפורטפוליו בתהליך |
| **Target CPA** | מספר או ריק | אופציונלי | מספר עשרוני חיובי עד 3 ספרות אחרי הנקודה, או ריק | לא נדרש לכל סוגי האופטימיזציה |

**פורמט ודרישות כלליות ל־Template:**
- סוגי נתונים:  
  - `Portfolio Name` – טקסט (Text)  
  - `Base Bid` – טקסט אם `"Ignore"`, אחרת מספר עשרוני בפורמט טקסט (ראו סעיף 5)  
  - `Target CPA` – ריק או מספר עשרוני בפורמט טקסט
- עמודת `Base Bid` חייבת להיות מלאה בכל שורה.
- קידוד קובץ: UTF-8 (Excel .xlsx).
- עמודות חייבות להופיע בדיוק בסדר הרשום.

---

## 3. Clean File (מוקאפ)

**מבנה עמודות:**  
זהה ל־Bulk File המקורי (אותן עמודות, אותו סדר).

**שינויים לעומת Bulk File:**
- בעמודת `Operation` – בכל השורות הערך יהיה `"Update"`.
- כל ערכי המספרים הסידוריים הארוכים (IDs למיניהם) יוצגו בפורמט טקסט כדי למנוע קיצור מדעי (Scientific Notation).
- כל הערכים יופיעו ממורכזים בעמודה (Horizontal Alignment: Center).
- ערכים מספריים יוצגו עם עד שלוש ספרות אחרי הנקודה (אם קיימת נקודה עשרונית).
- רוחב עמודות אחיד בכל הקובץ.

---

## 4. Working File (מוקאפ)

**מבנה עמודות:**  
זהה ל־Clean File, עם האפשרות להוסיף בהמשך עמודות עזר (לא מוגדר כרגע).  

**במוקאפ:**  
- מבנה זהה ל־Clean File (כולל כל הכללים בסעיף 3).
- עמודות עזר (Auxiliary Columns) יתווספו בשלבים מאוחרים יותר – אינן חלק מה־PRD הנוכחי.

---

## 5. כללי עיצוב ופורמט (Clean & Working)
- **מספרים סידוריים ארוכים** – יוגדרו כטקסט (Text) כדי למנוע הצגה ב־Scientific Notation.
- **יישור טקסט** – כל הערכים (טקסט ומספרים) ממורכזים.
- **רוחב עמודות** – אחיד בכל הקובץ.
- **פורמט מספרי** – עד שלוש ספרות אחרי הנקודה במידת הצורך.
- **Operation Column** – חובה שכל השורות יכילו `"Update"`.

---

## 6. חריגות
- במידה וחסרים ערכים בעמודות חובה (`Base Bid` ב־Template, `Operation` בפלט) – הקובץ ייפסל לפני שלב האופטימיזציה.
- אם קיימים ערכים לא חוקיים (למשל טקסט במקום מספר בעמודת מספר) – הקובץ יוחזר למשתמש עם הודעת שגיאה.

---

## 7. גרסת מסמך
- גרסה: 1.0 (מוקאפ)
- תאריך: YYYY-MM-DD
- מחבר: [שם מחבר]


## 8. פורמט שמות קבצי הפלט

- Working File: Auto Optimized Bulk | Working File | [YYYY-MM-DD] | [HH-MM]
- Clean File: Auto Optimized Bulk | Clean File | [YYYY-MM-DD] | [HH-MM]



### 9. Schema: Completion Template

Table: completion_template
- Portfolio Name: string, required, filled-by-system, immutable-on-user-side
- Base Bid: number (float), required, min=0
- Target CPA: number (float), optional, min=0, nullable

Constraints:
- Columns must exist exactly: ["Portfolio Name","Base Bid","Target CPA"]
- No row insertions/deletions by user; row count and order are system-defined
- Portfolio Name non-empty for all rows
- If Target CPA present → numeric and ≥ 0

### Completion Template – Step 2 בלבד
- סכמת העמודות זהה לטמפלט (Portfolio Name, Base Bid, Target CPA).
- Portfolio Name נכתב מראש ע"י המערכת עבור פריטים חסרים ואינו לשינוי.
- Base Bid – חובה למילוי בכל שורה.
- Target CPA – אופציונלי; ניתן להשאיר ריק כשלא נדרש.
- בעת העלאה, הקובץ מתמזג ל‑Virtual Map פנימי של Step 2. המסמך הזה אינו נקלט או מתמזג בשלב 3.

### 10. Completion Template
- **מבנה עמודות**: זהה בדיוק ל-Template File (סעיף 2)
  - Portfolio Name
  - Base Bid  
  - Target CPA
- **הבדל מהותי**: שמות הפורטפוליו ממולאים מראש ע"י המערכת ואינם ניתנים לעריכה
- **שימוש**: Step 2 בלבד, לצורך השלמת פורטפוליוז חסרים

### 11. Completion Template עם שגיאות ולידציה

כאשר מזוהות שגיאות בקומפלישן טמפלט שהועלה, המערכת מייצרת קומפלישן טמפלט חדש עם עמודה נוספת:

**מבנה עמודות:**
- Portfolio Name (טקסט) - ממולא מראש, לא ניתן לעריכה
- Base Bid (מספר/טקסט) - למילוי או תיקון ע"י המשתמש
- Target CPA (מספר) - אופציונלי
- Error (טקסט) - הודעת שגיאה: "Invalid value, please correct"

**התנהגות:**
- רק פורטפוליוז עם שגיאות מופיעים בקובץ זה
- העמודה Error מופיעה רק כשיש שגיאות
- המשתמש צריך לתקן את הערכים ולהעלות מחדש


