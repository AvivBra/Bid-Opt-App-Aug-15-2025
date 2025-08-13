# PRD – אפיון סטייל (UI Style Spec)

מסמך זה מגדיר **נראות**, **שפה עיצובית**, **פריסה** ו**כתיבה** לאפליקציית ה–Bid & Budget Optimizer. האפיון מתייחס **אך ורק** לסגנון, חלוקה למסכים/טאבים, טקסטים ומראה רכיבי ה–UI. הפונקציונליות בפועל מוגדרת במסמכים אחרים.

---

## 1) עקרונות-על
- **פשטות ודיוק**: UI נקי, ללא רעש; מעט טקסטים, מונחי עבודה ישירים.
- **ליניאריות שקופה**: שלושה שלבים קבועים ב–Tabs בראש המסך: **Upload → Validate → Output**.
- **קונסיסטנטיות**: אחידות בפדינג, טיפוגרפיה, כפתורים, הודעות סטטוס, ושמות רכיבים.
- **נגישות**: קונטרסט גבוה (ברירת המחדל של Streamlit), טקסטים קצרים, מצבי שגיאה גלויים.
- **מראה מקצועי**: ללא אימוג'י, ללא אייקונים, ממשק טקסט בלבד.

---

## 2) בסיס וערכי-יסוד (Foundations)
### 2.1 Theme & Page
- מסגרת: **Streamlit**, `st.set_page_config(layout="wide", page_title="Bid Optimizer – Bulk", initial_sidebar_state="collapsed")`.
- **Layout**: Centered (default).

### 2.2 צבעים (מושענים על ברירת המחדל של Streamlit)
- **טקסט ראשי**: כהה/שחור.
- **כותרות**: כהה.
- **כפתור ראשי**: אדום (#DC3545).
- **מצבים**:
  - Error: אדום.
  - Warning: צהוב/ענברי.
  - Info: כחול/תכלת.
  - Success: ירוק.
  - Notice מיוחד (חישוב): **ורוד**.

> הערה: שימוש ברכיבי `st.error / st.warning / st.info / st.success` לשמירת אחידות גוונים ונגישות.

### 2.3 טיפוגרפיה
- **Title (H1)**: שימוש ב–`st.title`.
- **Subheader (H3)**: `st.subheader`.
- **Body**: טקסט קצר, משפטים קצרים, אותיות רישיות בתחילת תוויות וכפתורים.
- **שפה**: אנגלית בלבד בכל האפליקציה (UI, הודעות, קבצים, תיעוד).

### 2.4 מרווחים ורדיוסים
- **Spacing Scale**: 8px, 12px, 16px, 24px (להתאמה בכלי).
- **Padding פנימי לרכיב/קונטיינר**: 16–24px.
- **Gap בין רכיבי טופס**: 12–16px.
- **Rounded**: ברירת מחדל עדינה של Streamlit (ללא קסטומיזציה נוספת).

### 2.5 אייקונים ואימוג'י
- **אסור להשתמש באייקונים או אימוג'י בכל הממשק**.
- **טקסט נקי בלבד** לכל הכפתורים, הודעות וכותרות.
- **ללא סמלים גרפיים** - רק טקסט מקצועי.

---

## 3) פריסה (Layout)
### 3.1 מבנה עמוד
- **Header**:
  - `st.title("Bid Optimizer – Bulk File")` בחלק העליון, מיושר שמאלה.
  - מתחתיו (אופציונלי): פס התקדמות/טקסט מצב קצר (לפי שלב).
- **Tabs** (בראש הדף, בקו אחד):  
  1. **Upload**  
  2. **Validate**  
  3. **Output**

### 3.2 טאב Upload
- **Grid**: שתי עמודות שוות: `st.columns([1,1])`.
- **עמודה שמאל**:
  - `st.subheader("Files")`
  - **Download Template** (כפתור הורדה ללא אייקון) עם Tooltip: "Demo template for mockup only".
  - **File Uploader – Template**  
    - Label: `Upload Template (xlsx/csv)`  
    - קלט: `.xlsx, .csv`
  - **File Uploader – Bulk**  
    - Label: `Upload Bulk (xlsx/csv, sheet: Sponsored Products Campaigns)`  
    - קלט: `.xlsx, .csv`
- **עמודה ימין**:
  - מקום לתצוגת סיכום קבצים, טקסטי עזר, או הנחיות קצרות.

### 3.3 טאב Validate
- **כותרת משנה**: `st.subheader("Validation Summary")`.
- **סיכומי קבצים שהועלו**: רכיב תצוגה מינימליסטי:  
  - שם קובץ ב–bold (למשל: `**Template:** filename.xlsx`), או `not uploaded`.
- **תצוגת Missing/Surplus**:
  - Missing Count: מספר בולט בשורה נפרדת.
  - Surplus List: רשימה (תבליטים/שורות) במכלול ממוסגר.
  - **Copy to Clipboard**: כפתור קטן/משני לצורך העתקה.
- **הודעות סטטוס**:
  - שימוש ב–`st.error / st.warning / st.info / st.success` לפי הקונטקסט.
- **כפתורי ניווט**:
  - Primary: "Continue".
  - Secondary (אם קיים): "Back".

### 3.4 טאב Output
- **כותרת משנה**: `st.subheader("Output")`.
- **מצב ריצה**: טקסט/אינדיקטור קצר (אופציונלי Progress Bar בזמן עיבוד).
- **תוצאות עיקריות**: שורות מידע קצרות (updated / failed / processed).
- **כפתורי הורדה**:
  - Primary: `Download Working File`
  - Primary: `Download Clean File`
- **כפתור עיבוד נוסף**:
  - Secondary/Danger-Lite: `Full Reset` / `Process Again`
  - טקסט עזר קצר (אם רלוונטי): "Clears all session state".

---

## 4) רכיבי UI (קטלוג מצומצם)
### 4.1 File Uploader
- **Label** קצר וברור (ראה 3.2).
- מדריך פורמטים בסוגריים.
- מצב "לא הועלה קובץ" מצוין בטקסט אפור.

### 4.2 Download Button
- טקסט פעיל (Imperative): "Download Template", "Download Clean File".
- Tooltip/Help קצר כשצריך.
- ללא אייקונים או אימוג'י.

### 4.3 Messages (Alerts)
- **Error (אדום)**: עוצר פעולה/שלב. טקסט קצר, חד וברור.  
  דוגמה: `File "template.csv" titles are incorrect.`
- **Warning (צהוב)**: התרעה שאינה חוסמת.  
- **Info (כחול)**: מידע ניטרלי/הסבר.  
- **Success (ירוק)**: השלמה מוצלחת.  
- **Notice מיוחד – ורוד**: הודעת "Please note" ייעודית לשגיאות חישוב (שלב 3).

### 4.4 Lists & Counters
- **Surplus**: רשימת תבליטים נקייה; אם ארוכה – בתוך קונטיינר עם גלילה אנכית עדינה.
- **Counters**: מספרים בולטים בשורה עצמאית (Bold + מרווח מעל/מתחת של 8–12px).

### 4.5 Buttons
- **Primary**: פעולה ראשית בשלב (Continue / Download) - צבע אדום.
- **Secondary**: חזרה/Reset/Copy - צבע אפור.
- **States**: Disabled/Loading בהתאם למצב (Streamlit default).

### 4.6 Progress
- שימוש בפס התקדמות/טקסט מצב קצר בלבד כשיש פעולה נמשכת.

### 4.7 Tables / Summaries (אם נדרשות)
- טבלה נקייה, ללא גבולות כבדים; רוחב עמודות אוטומטי; יישור מרכז/שמאל לפי סוג הערך.
- שורת כותרת מודגשת.

---

## 5) שפה ותוכן (UX Writing)
- **טון**: תכליתי, לא רשמי מדי, "Product voice".
- **קצר ומדויק**: עד 8–12 מילים לפריט UI.
- **קונסיסטנטיות**:
  - פעלים בכותרות כפתורים ("Upload", "Download", "Continue", "Reset").
  - אות רישית בתחילת כל Label/כפתור.
  - ללא אימוג'י או אייקונים בטקסטים.
- **מיקרוקופי לדוגמה**:
  - Upload: `Upload Template (xlsx/csv)`
  - Upload: `Upload Bulk (xlsx/csv, sheet: Sponsored Products Campaigns)`
  - Download: `Download Template` / `Download Clean File` / `Download Working File`
  - Validate: `Missing portfolios: 12` / `Surplus portfolios (4): ...`
  - Output: `Please note: 7 calculation errors in Portfolio Bid Optimization.`

---

## 6) מצבי שגיאה/אזהרה/מידע – סגנון תצוגה
- **Error (אדום)**: בלוק מלא (Streamlit error), ללא אייקון, טקסט בשורה אחת/שתיים.
- **Warning (צהוב)**: בלוק מלא, טקסט הסבר קצר.
- **Info (כחול)**: בלוק מלא למידע ניטרלי.
- **Notice ורוד (שלב 3)**: "Please note: <N> calculation errors in <Optimization_Type>."  
  מוצג **במקביל** לכפתורי ההורדה, אינו חוסם הורדה.

---

## 7) רספונסיביות
- **Centered** כברירת מחדל; שני טורים ב–Upload מתכווצים לטור יחיד במסכים צרים.
- רכיבי טקסט/כפתורים נשארים בשורה אחת ככל האפשר; אם נשבר לשתי שורות – הוספת מרווח אנכי קטן (8px).

---

## 8) נגישות
- הסתמכות על רכיבי Streamlit להבטחת קונטרסט/ניווט מקלדת.
- הימנעות מטקסטים ארוכים; כל הודעה ≤ שתי שורות כשאפשר.
- Tooltips מסייעים אך לא קריטיים להבנה.

---

## 9) "עשה ואל תעשה"
**עשה**
- שמור על Labels קצרים ועקביים.
- השתמש תמיד ברכיבי ההודעות הסטנדרטיים.
- סדר ליניארי: Upload → Validate → Output.
- השתמש בטקסט נקי ומקצועי בלבד.

**אל תעשה**
- אל תוסיף טקסטים דקלרטיביים ארוכים.
- אל תערבב שפות באותו רכיב.
- אל תחליף את סדר הטאבים.
- **אל תשתמש באייקונים או אימוג'י**.

---

## 10) טקסטים מחייבים לפי שלב (תבניות)
### Upload
- Title: `Bid Optimizer – Bulk File`
- Subheader: `Files`
- Buttons:
  - `Download Template`
- Uploaders:
  - `Upload Template (xlsx/csv)`
  - `Upload Bulk (xlsx/csv, sheet: Sponsored Products Campaigns)`

### Validate
- Subheader: `Validation Summary`
- Counters/Lists:
  - `Missing portfolios: <N>`
  - `Surplus portfolios (<N>):`
- Buttons:
  - Primary: `Continue`
  - Secondary: `Back`
  - Utility (אם יש): `Copy`

### Output
- Subheader: `Output`
- Notices:
  - ורוד: `Please note: <N> calculation errors in <Optimization_Type>.`
  - Info: `Bids outside range: <N> rows with bid <0.02 or >1.25.`
- Buttons:
  - Primary: `Download Working File`
  - Primary: `Download Clean File`
  - Secondary: `Full Reset`

---

## 11) הרחבות עתידיות (לא מחייב במוקאפ)
- Tooltip קבועים לרכיבים רגישים (למשל, "sheet: Sponsored Products Campaigns").
- פס התקדמות לינארי גלובלי בראש המסך.

---

## 12) גרסה
- גרסת מסמך: **UI-Style v1.1**
- תקף ל–Mockup ול–MVP הראשון
- עדכון אחרון: הוספת איסור שימוש באייקונים ואימוג'י, שינוי צבע כפתורים ראשיים לאדום