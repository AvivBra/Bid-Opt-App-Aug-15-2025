# חוקי תקשורת עם המשתמשת

## חוקי יסוד

### 1. אסור קוד בצאט
- קוד רק בארטיפקטים
- המשתמשת לא מבינה קוד
- המשתמשת רק מעתיקה ומדביקה

### 2. עברית תמיד
- כל ההסברים בעברית
- מונחים טכניים בתעתיק עברי (פורטפוליו, אנטיטי, קמפיין)
- לא לערבב אנגלית באמצע משפטים

### 3. הנחיות פשוטות
- רק פעולות של העתק/הדבק/שמור
- לא לבקש למצוא שורות
- לא לבקש לערוך קוד

### 4. הסברים ברורים
- להסביר מה השתנה בלי להראות קוד
- להסביר איפה הבעיה בלי מספרי שורות
- להסביר בעברית פשוטה מה התיקון עושה

## דוגמאות

**נכון:**
"הפונקציה מסננת שורות שבהן אנטיטי שווה לקיוורד"

**לא נכון:**
"הפונקציה מסננת שורות שבהן Entity = Keyword"

**נכון:**
"תיקנתי את הבדיקה כך שתחפש התאמה מדויקת"

**לא נכון:**
"שיניתי בשורה 45 מ-contains ל-isin"


# חוקי הוספת דיבוג לקוד

## 1. מטרת הדיבוג
- לזהות בדיוק היכן הסינון נכשל
- להציג את מספר השורות אחרי כל שלב עיבוד
- לראות את הכל בטרמינל בלבד

## 2. מיקום ההדפסות
- **רק בטרמינל** - משתמשים ב-print() רגיל
- **לא ב-UI** - לא משתמשים ב-st.write() או st.info()
- המשתמש לא רואה כלום באפליקציה

## 3. פורמט אחיד לכל שורת דיבוג
```python
# DEBUG MODE
print(f"🔍 DEBUG [{שם_הקובץ}] {תיאור_השלב}: {len(df)} rows")
# DEBUG MODE
```

## 4. סימון ברור
- כל שורת debug מוקפת בהערות `# DEBUG MODE` לפני ואחרי
- חובה בשורה נפרדת לפני ואחרי
- מאפשר מחיקה קלה עם חיפוש של "# DEBUG MODE"

## 5. דוגמה נכונה
```python
# DEBUG MODE
print(f"🔍 DEBUG [optimizer.py] After apply_initial_filters: {len(filtered_df)} rows")
# DEBUG MODE
```

## 6. מה להדפיס
- שם הקובץ
- שם השלב/פונקציה
- מספר שורות נוכחי
- אם רלוונטי: מספר שורות שהוסרו

## 7. איפה להוסיף
- אחרי כל פונקציית סינון
- לפני החזרת תוצאה סופית
- במקרי שגיאה או חריגה

## 8. ניקוי בסיום
- חיפוש בכל הפרויקט: "# DEBUG MODE"
- מחיקת כל הבלוק (3 שורות: הערה + print + הערה)
- או: הוספת משתנה DEBUG = False בראש הקובץ

## 9. קבצים לדיבוג
1. optimizers/zero_sales/optimizer.py
2. optimizers/zero_sales/processors/sheet_creator.py
3. optimizers/zero_sales/processors/data_cleaner.py
4. ui/step2_processing.py (אם צריך)

## 10. אסור
- להשאיר את הדיבוג בקוד הסופי
- להדפיס מידע רגיש
- להדפיס יותר מדי (רק את החשוב)
- לשנות את הלוגיקה של הקוד


# Code Generation Rule

When modifying or creating code for this project:

**Do not add any elements, features, or changes that were not explicitly requested.**

Make only the specific changes asked for. Nothing more.