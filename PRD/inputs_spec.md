# קובץ אפיון קלטים – Bid & Budget Optimizer

## סקירה כללית
האפליקציה מקבלת שלושה סוגי קלטים בשלב ה־Upload (שלב 1).  
הקלטים נדרשים כדי להפעיל את תהליך ולידציית הפורטפוליוז (שלב 2) ואת שלב הפקת הפלטים (שלב 3).

---

## 1. Bulk File

### תיאור
- קובץ Amazon Ads Bulk, בפורמט **Excel (.xlsx)** או **CSV**.
- כולל מספר לשוניות (Sheets).
- **לשונית חובה לעיבוד**: `Sponsored Products Campaigns`.

### מגבלות
- גודל מקסימלי: **40MB** – אם גדול יותר → הודעת שגיאה.
- עד **500,000 שורות**.
- אם יש יותר מלשונית אחת עם אותו שם → הודעת שגיאה.
- חייב להכיל את כל הכותרות הבאות, **בדיוק באיות ובסדר הרשום**:

### שמות העמודות
- יהיו בדיוק כדלהלן:
Product
Entity
Operation
Campaign ID
Ad Group ID
Portfolio ID
Ad ID
Keyword ID
Product Targeting ID
Campaign Name
Ad Group Name
Campaign Name (Informational only)
Ad Group Name (Informational only)
Portfolio Name (Informational only)
Start Date
End Date
Targeting Type
State
Campaign State (Informational only)
Ad Group State (Informational only)
Daily Budget
SKU
ASIN
Eligibility Status (Informational only)
Reason for Ineligibility (Informational only)
Ad Group Default Bid
Ad Group Default Bid (Informational only)
Bid
Keyword Text
Native Language Keyword
Native Language Locale
Match Type
Bidding Strategy
Placement
Percentage
Product Targeting Expression
Resolved Product Targeting Expression (Informational only)
Impressions
Clicks
Click-through Rate
Spend
Sales
Orders
Units
Conversion Rate
ACOS
CPC
ROAS

---

## 2. Template File

### תיאור
- קובץ Template שמורד מהמערכת על ידי המשתמש.
- לשונית אחת בלבד (השם לא משנה).

### מבנה הכותרות
- שלוש עמודות חובה, בדיוק בשם הבא:
Portfolio Name
Base Bid
Target CPA



### שימוש
- המשתמש ממלא בו את כל הפורטפוליוז הקיימים ב־Bulk File, עם ערכי Base Bid ו־Target CPA.
- ניתן להזין את הערך `"Ignore"` בעמודת `Base Bid` אם רוצים שהמערכת תדלג על הפורטפוליו.

המילוי של עמודת Base Bid הוא חובה. עמודת Target CPA היא אופציונלית — היא תימלא רק אם סוג האופטימיזציה שנבחר דורש אותה.




---

## 3. Optimization Checklist

### תיאור
- רשימת סוגי האופטימיזציה הנתמכים.
- במוקאפ – יש סוג אחד בלבד:  
- זה צ׳קליסט שמופיע ב ui והמשתמש מסמן את סוגי האופטימיזציות שהוא רוצה לבצע

### שימוש
- המשתמש חייב לבחור לפחות סוג אופטימיזציה אחד כדי להתקדם.


---

## 4. Completion Template (קלט‑פלט למילוי ידני)

במקרה של חוסרים בשלב 2, המערכת מפיקה קובץ Completion Template להשלמה. לקובץ זה תמיד שלוש עמודות:
- Portfolio Name (ממולא מראש ע"י המערכת)
- Base Bid (למילוי ע"י המשתמש – חובה)
- Target CPA (למילוי ע"י המשתמש – אופציונלי, רק כשנדרש)

המשתמש אינו מוסיף או מסיר שורות; המערכת כותבת את כל שמות הפורטפוליוז החסרים. לאחר ההעלאה, הנתונים מתמזגים לתוך “Virtual Map” פנימי של שלב 2. 
Completion Template הוא מנגנון של **Step 2 בלבד**. בסיום Step 2 ה‑Virtual Map מלא, ו‑Step 3 משתמש בו כקלט מוכן, ללא העלאות/מיזוגים נוספים.


מטרת הקובץ: הקובץ הזה נוצר רק אם בשלב 2 חסר למערכת מידע על פורטפוליוז מסוימים בטמפלט המקורי המלא שהעלה המשתמש. אז היא מייצרת את הטמפלט המשלים לצורך השלמת מידע. המטרה היא להציג למשתמש את רשימת הקמפיינים החסרים (לפי "המפה 
הווירטואלית" שהמערכת מייצרת), כך שהמשתמש ימלא רק ערכי ביד ו/או TargetCPA היכן שנדרש.

מבנה עמודות (בדיוק כך, כולל שמות הכותרות):
- PortfolioName (טקסט) — שם הפורטפוליו שאליו הקמפיין ישויך. עמודה זו מתמלאת אוטומטית ע"י המערכת ואינה לעריכה.
- BaseBid (מספר עשרוני ≥ 0) — ערך חיובי או 0. חובה למלא עבור כל שורת קמפיין המוצגת.
- TargetCPA (מספר עשרוני ≥ 0, אופציונלי) — ימולא רק כאשר יש צורך בכללי אופטימיזציה מבוססי CPA. אם לא נדרש, להשאיר ריק.

התנהגות וסמנטיקה:
- המערכת מייצרת את כל שורות הקמפיינים החסרים ומכניסה את הערך ב‑PortfolioName עבור כל שורה. המשתמש אינו מוסיף/מוחק שורות ואינו משנה את "PortfolioName".
- המשתמש ממלא:
  - BaseBid — תמיד.
  - TargetCPA — רק במקרים בהם נדרש CPA (אחרת להשאיר ריק).
- המערכת תתמוך בייבוא הקובץ חזרה ותבצע ולידציות:
  - קיום שלושת העמודות בשם המדויק: PortfolioName, BaseBid, TargetCPA.
  - BaseBid מספרי ובלתי־שלילי.
  - TargetCPA, אם מולא, מספרי ובלתי־שלילי.
  - אין שינוי/מחיקה של שורות קיימות ואינן מכילות ערכי PortfolioName ריקים.

פורמט קובץ:
- Excel (.xlsx) או CSV עם כותרות מדויקות כנ"ל.
- קידוד UTF‑8 עבור CSV.

דוגמא קצרה:
PortfolioName | BaseBid | TargetCPA
------------- | ------- | ---------
Kids‑Brand‑US | 0.55    | 4.20
Kids‑Brand‑US | 0.35    | 
Supp‑EU       | 0.62    | 


### מבנה עמודות
**זהה בדיוק ל-Template File:**
- Portfolio Name (טקסט) - ממולא מראש ע"י המערכת, לא ניתן לעריכה
- Base Bid (מספר) - למילוי ע"י המשתמש, חובה
- Target CPA (מספר) - למילוי ע"י המשתמש, אופציונלי
