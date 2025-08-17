# מפרט קלט/פלט - Bid Optimizer

## 1. Template File - קלט

### מבנה
- **פורמט:** Excel (.xlsx) או CSV
- **גודל מקסימלי:** 40MB
- **sheets:** 1 (כל שם)
- **קידוד:** UTF-8

### עמודות (בדיוק בסדר הזה)
| # | שם עמודה | סוג | חובה | ערכים תקינים |
|---|----------|-----|-------|---------------|
| 1 | Portfolio Name | String | כן | כל טקסט |
| 2 | Base Bid | Number/String | כן | 0.00-999.99 או "Ignore" |
| 3 | Target CPA | Number | לא | 0.00-9999.99 או ריק |

### דוגמה
```
Portfolio Name    | Base Bid | Target CPA
-----------------|----------|------------
Kids-Brand-US    | 1.25     | 5.00
Kids-Brand-EU    | 0.95     | 
Supplements-US   | Ignore   | 
Supplements-EU   | 2.10     | 8.50
```

### ולידציות
- אין כפילויות ב-Portfolio Name
- Base Bid חייב ערך בכל שורה
- אם Base Bid = "Ignore", הפורטפוליו לא נבדק

## 2. Bulk File - קלט

### מבנה
- **פורמט:** Excel (.xlsx) או CSV
- **גודל מקסימלי:** 40MB
- **מספר שורות מקסימלי:** 500,000
- **Sheet נדרש:** "Sponsored Products Campaigns"
- **קידוד:** UTF-8

### 48 עמודות (בדיוק בסדר הזה)
```
1. Product
2. Entity
3. Operation
4. Campaign ID
5. Ad Group ID
6. Portfolio ID
7. Ad ID
8. Keyword ID
9. Product Targeting ID
10. Campaign Name
11. Ad Group Name
12. Campaign Name (Informational only)
13. Ad Group Name (Informational only)
14. Portfolio Name (Informational only)
15. Start Date
16. End Date
17. Targeting Type
18. State
19. Campaign State (Informational only)
20. Ad Group State (Informational only)
21. Daily Budget
22. SKU
23. ASIN
24. Eligibility Status (Informational only)
25. Reason for Ineligibility (Informational only)
26. Ad Group Default Bid
27. Ad Group Default Bid (Informational only)
28. Bid
29. Keyword Text
30. Native Language Keyword
31. Native Language Locale
32. Match Type
33. Bidding Strategy
34. Placement
35. Percentage
36. Product Targeting Expression
37. Resolved Product Targeting Expression (Informational only)
38. Impressions
39. Clicks
40. Click-through Rate
41. Spend
42. Sales
43. Orders
44. Units
45. Conversion Rate
46. ACOS
47. CPC
48. ROAS
```

### סינון אוטומטי (Bulk Cleaning)
המערכת מסננת רק שורות ש:
- Entity = "Keyword" או "Product Targeting" או "Bidding Adjustment"
- State = "enabled"
- Campaign State (Informational only) = "enabled"
- Ad Group State (Informational only) = "enabled"

## 3. Working File - פלט

### מבנה
- **פורמט:** Excel (.xlsx) בלבד
- **שם קובץ:** `Auto Optimized Bulk | Working | YYYY-MM-DD | HH-MM.xlsx`
- **דוגמה:** `Auto Optimized Bulk | Working | 2024-01-15 | 14-30.xlsx`

### Sheets
לכל אופטימיזציה שנבחרה:

**Zero Sales - 3 sheets:**
1. `Clean Zero Sales` - Keywords/Product Targeting עם עמודות עזר
2. `Bidding Adjustment Zero Sales` - Bidding Adjustments בלבד
3. `Working Zero Sales` - זהה ל-Clean (שמור לעתיד)

**אופטימיזציות אחרות - 2 sheets לכל אחת:**
1. `Clean {OptimizationName}`
2. `Working {OptimizationName}`

### עמודות עזר (Zero Sales בלבד)
מוספות משמאל לעמודה Bid (רק בלשונית הראשית):
- Max BA
- Base Bid
- Target CPA
- Adj. CPA
- Old Bid
- calc1
- calc2

### תוכן
- **Clean sheets:** 48 עמודות מקוריות + עמודות עזר (באופטימיזציות רלוונטיות)
- **Working sheets:** זהה ל-Clean (בגרסה עתידית יכלול עמודות נוספות)
- **Bidding Adjustment sheets:** 48 עמודות מקוריות בלבד, ללא עמודות עזר
- **כל השורות:** Operation = "Update"

### סימון שגיאות
- שורות עם Bid < 0.02 או Bid > 1.25 מסומנות בצבע ורוד
- שורות עם שגיאת חישוב מסומנות בצבע ורוד

## 4. Clean File - פלט

### מבנה
- **פורמט:** Excel (.xlsx) בלבד
- **שם קובץ:** `Auto Optimized Bulk | Clean | YYYY-MM-DD | HH-MM.xlsx`
- **דוגמה:** `Auto Optimized Bulk | Clean | 2024-01-15 | 14-30.xlsx`

### Sheets
לכל אופטימיזציה שנבחרה:

**Zero Sales - 2 sheets:**
1. `Clean Zero Sales` - Keywords/Product Targeting עם עמודות עזר
2. `Bidding Adjustment Zero Sales` - Bidding Adjustments בלבד

**אופטימיזציות אחרות - 1 sheet לכל אחת:**
- `Clean {OptimizationName}`

### תוכן
- זהה לWorking File (כרגע)
- בעתיד: ללא עמודות עזר

## 5. Empty Template - להורדה

### מבנה
```
Portfolio Name | Base Bid | Target CPA
---------------|----------|------------
               |          |
```
- 3 עמודות
- 0 שורות נתונים
- רק כותרות

## 6. פורמט נתונים

### מספרים
- **IDs:** נשמרים כטקסט למניעת scientific notation
- **Bid:** עד 3 ספרות אחרי הנקודה (0.000)
- **Budget:** עד 2 ספרות אחרי הנקודה (0.00)
- **Percentages:** כמספר עשרוני (0.15 = 15%)

### תאריכים
- **פורמט:** MM/DD/YYYY
- **דוגמה:** 01/15/2024

### טקסט
- **קידוד:** UTF-8
- **תווים מיוחדים:** נתמכים
- **Case sensitive:** כן

## 7. מגבלות גודל

### קבצי קלט
- **מקסימום:** 40MB
- **מקסימום שורות:** 500,000

### קבצי פלט
- **אין מגבלה** (תלוי בקלט)
- **צפוי:** 1.5x גודל הקלט

## 8. טיפול בשגיאות קלט

### Template File
| בעיה | טיפול |
|------|--------|
| עמודות חסרות | שגיאה: "Missing columns: {names}" |
| סדר עמודות שגוי | שגיאה: "Wrong column order" |
| קובץ ריק | שגיאה: "Template is empty" |
| Base Bid לא תקין | שגיאה: "Invalid Base Bid in row {n}" |

### Bulk File
| בעיה | טיפול |
|------|--------|
| Sheet חסר | שגיאה: "Sheet 'Sponsored Products Campaigns' not found" |
| 48 עמודות חסרות | שגיאה: "Missing required columns" |
| מעל 500K שורות | שגיאה: "File exceeds 500,000 rows" |
| קובץ ריק אחרי סינון | שגיאה: "No valid rows after filtering" |

## 9. הודעות למשתמש

### Zero Sales Optimization
| מצב | הודעה |
|-----|--------|
| אין Bidding Adjustment | "Note: No Bidding Adjustment rows found" |
| ערכי Bid חריגים | "{X} rows below 0.02, {Y} rows above 1.25" |
| שגיאות חישוב | "{Z} rows with calculation errors" |