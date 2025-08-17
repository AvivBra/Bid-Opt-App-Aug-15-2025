# לוגיקת אופטימיזציית זירו סיילס

## תהליך האופטימיזציה - 4 שלבים

### שלב 1: ניקוי הדאטה

משאירים רק שורות שעונות על **כל** התנאים הבאים:

1. **Units = 0**  
   רק שורות שלא נמכרו בהן יחידות כלל

2. **פורטפוליו לא בשימוש פלאט**  
   השדה `Portfolio Name (Informational only)` **לא** שווה לאף אחד מהערכים:
   - Flat 30
   - Flat 25
   - Flat 40
   - Flat 25 | Opt
   - Flat 30 | Opt
   - Flat 20
   - Flat 15
   - Flat 40 | Opt
   - Flat 20 | Opt
   - Flat 15 | Opt

### שלב 2: הפרדת Bidding Adjustment

1. **יצירת לשונית נפרדת**  
   כל השורות שה-Entity שלהן הוא "Bidding Adjustment" מועברות ללשונית נפרדת

2. **שם הלשונית**  
   "Bidding Adjustment Zero Sales"

3. **הלשונית הראשית**  
   נשארות רק שורות עם Entity = "Keyword" או "Product Targeting"

4. **טיפול במקרה חסר**  
   אם אין שורות Bidding Adjustment:
   - הודעה למשתמש: "Note: No Bidding Adjustment rows found"
   - Max BA יקבל ערך ברירת מחדל של 1

### שלב 3: הוספת עמודות עזר וחישובן

הוספת עמודות עזר **משמאל לעמודה Bid** (רק בלשונית הראשית, לא ב-Bidding Adjustment):

1. **Max BA** - הערך המקסימלי מעמודה Percentage בשורות שבהן:
   - Entity = "Bidding Adjustment"
   - Campaign ID = Campaign ID של השורה הנוכחית
   - אם אין התאמות: ערך ברירת מחדל = 1

2. **Base Bid** - העתקה מקובץ Template לפי שם Portfolio

3. **Target CPA** - העתקה מקובץ Template לפי שם Portfolio

4. **Adj. CPA** = Target CPA × (1 + Max BA/100)

5. **Old Bid** = Bid (שמירת הערך המקורי)

6. **calc1** - חישוב ביניים (ראה מקרים ג-ד)

7. **calc2** - חישוב ביניים (ראה מקרים ג-ד)

### שלב 4: חישוב הביד החדש

החישוב מתחלק ל-4 מקרים:

#### מקרה א
**תנאי:**
- Target CPA חסר
- בעמודה Campaign Name (Informational only) **מופיע** הרצף "up and"

**חישוב:**
- Bid = Base Bid × 0.5

#### מקרה ב
**תנאי:**
- Target CPA חסר
- בעמודה Campaign Name (Informational only) **לא מופיע** הרצף "up and"

**חישוב:**
- Bid = Base Bid

#### מקרה ג
**תנאי:**
- Target CPA מופיע
- בעמודה Campaign Name (Informational only) **מופיע** הרצף "up and"

**חישובים:**
- calc1 = Adj. CPA × 0.5 / (Clicks + 1)
- calc2 = calc1 - Base Bid × 0.5

**חישוב Bid:**
- אם calc1 ≤ 0: **Bid = calc2**
- אם calc1 > 0: **Bid = Base Bid × 0.5**

#### מקרה ד
**תנאי:**
- Target CPA מופיע
- בעמודה Campaign Name (Informational only) **לא מופיע** הרצף "up and"

**חישובים:**
- calc1 = Adj. CPA / (Clicks + 1)
- calc2 = calc1 - Base Bid / (1 + Max BA / 100)

**חישוב Bid:**
- אם calc1 ≤ 0: **Bid = calc2**
- אם calc1 > 0: **Bid = Base Bid / (1 + Max BA / 100)**

## שלב 5: סימון שגיאות וערכים חריגים

**סימון בצבע ורוד** לכל השורות שבהן:
- Bid < 0.02 (below minimum)
- Bid > 1.25 (above maximum)
- Bid calculation failed (formula error)

**User notification:**
- Total number of rows with issues
- Details: "{X} rows below 0.02, {Y} rows above 1.25, {Z} rows with calculation errors"

## מבנה קבצי הפלט

### Working File
- **לשונית 1:** "Clean Zero Sales" - שורות Keyword ו-Product Targeting עם כל העמודות כולל עמודות העזר
- **לשונית 2:** "Bidding Adjustment Zero Sales" - שורות Bidding Adjustment ללא עמודות עזר

### Clean File  
- **לשונית 1:** "Clean Zero Sales" - שורות Keyword ו-Product Targeting עם כל העמודות כולל עמודות העזר
- **לשונית 2:** "Bidding Adjustment Zero Sales" - שורות Bidding Adjustment ללא עמודות עזר

**הערה:** כרגע שני הקבצים זהים. בעתיד Clean File לא יכלול עמודות עזר.