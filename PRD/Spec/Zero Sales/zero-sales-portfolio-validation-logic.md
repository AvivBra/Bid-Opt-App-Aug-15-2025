# לוגיקת ולידציה של פורטפוליוז

# הערה חשובה: ולידציה ספציפית ל-Zero Sales
קובץ זה מתאר את לוגיקת הוולידציה של פורטפוליוז עבור אופטימיזציית Zero Sales בלבד.
אופטימיזציות אחרות עשויות לא לבצע בדיקת פורטפוליוז כלל, או לבצע בדיקות שונות.

## רקע
הולידציה בודקת האם כל הפורטפוליוז שנמצאים בקובץ Bulk (אחרי הניקוי) קיימים בקובץ Template.

## חשוב
**הולידציה מתבצעת רק על לשונית Targets (שמכילה Keyword + Product Targeting בלבד)**

## תהליך הולידציה

### שלב 1: חילוץ פורטפוליוז מ-Template
- לוקחים את כל הפורטפוליוז מעמודת Portfolio Name
- **לא כוללים** פורטפוליוז שה-Base Bid שלהם הוא "Ignore"
- שומרים רשימה של הפורטפוליוז התקפים

### שלב 2: חילוץ פורטפוליוז מלשונית Targets בלבד
- **רק מלשונית Targets** (לא מ-Product Ads, לא מ-Bidding Adjustments)
- לוקחים ערכים ייחודיים מעמודת Portfolio Name (Informational only)
- מסירים ערכים ריקים

### שלב 3: השוואה
- מוצאים פורטפוליוז שקיימים ב-Targets אבל לא ב-Template
- הרשימה הזו נקראת "missing portfolios"

### שלב 4: סינון פורטפוליוז מותרים
פורטפוליוז הבאים מותרים להיות חסרים (לא חוסמים עיבוד):
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

אם פורטפוליו חסר נמצא ברשימה הזו, הוא לא נחשב כבעיה.

### שלב 5: קביעת תוצאה

**תקין:**
- אם אין פורטפוליוז חסרים (או רק כאלה מהרשימה המותרת)
- הודעה: "All portfolios valid"
- מאפשר המשך לעיבוד

**לא תקין:**
- אם יש פורטפוליוז חסרים שלא ברשימה המותרת
- הודעה: "Missing portfolios found - Reupload Full Template: {missing template list}"
- מציג רשימת הפורטפוליוז החסרים על המסך
- חוסם המשך לעיבוד
- מאפשר העלאה מחודשת של קובץ Template
- העלאה מחודשת מאפסת את כל התהליך ומתחילה בדיקה מחדש

## דוגמה

### Template:
- Portfolio A (Base Bid: 1.25)
- Portfolio B (Base Bid: 0.95)
- Portfolio C (Base Bid: Ignore)
- Portfolio D (Base Bid: 2.10)

### Targets (אחרי ניקוי):
- Portfolio A - 100 שורות
- Portfolio B - 50 שורות
- Portfolio D - 75 שורות
- Portfolio E - 25 שורות
- Flat 30 - 10 שורות

### תוצאה:
- **חסר:** Portfolio E (לא בTemplate)
- **מותר:** Flat 30 (ברשימה המותרת)
- **מסקנה:** לא תקין - חוסם עיבוד
- **הודעה:** "Missing portfolios found (1): Portfolio E"