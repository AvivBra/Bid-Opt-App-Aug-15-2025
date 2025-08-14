# אפיון ניקוי ראשוני - שלב 2 (Validate Portfolios)

## 1. מטרה
סינון וניקוי של נתוני ה-Bulk File לפני ביצוע השוואת הפורטפוליוז, כדי להשאיר רק את השורות הרלוונטיות לעיבוד.

## 2. תהליך הניקוי

### 2.1 בחירת לשונית
- המערכת עובדת **אך ורק** עם הלשונית `Sponsored Products Campaigns`
- כל שאר הלשוניות בקובץ ה-Bulk מתעלמות לחלוטין

### 2.2 קריטריונים לסינון שורות

המערכת משאירה שורה **רק אם כל התנאים הבאים מתקיימים**:

#### תנאי 1: סוג Entity
```
Entity = "Product Targeting" 
OR 
Entity = "Keyword"
```

#### תנאי 2: סטטוס פעיל
כל שלושת השדות הבאים חייבים להיות `"enabled"`:
- `State = "enabled"`
- `Campaign State (Informational only) = "enabled"`
- `Ad Group State (Informational only) = "enabled"`

#### תנאי 3: פורטפוליו קיים ב-Virtual Map
- ערך השדה `Portfolio Name (Informational only)` **חייב להופיע** ב-Virtual Map הנוכחי
- פורטפוליוז שנמחקו מה-Virtual Map (בגלל Ignore) לא ייכללו
- השוואה case-sensitive (רגיש לאותיות גדולות/קטנות)

**הערה**: Virtual Map מתעדכן דינמית עם כל העלאת Completion Template, כולל מחיקת פורטפוליוז עם "Ignore"

## 4. דוגמאות

### דוגמה לשורה שתישמר:
| Entity | State | Campaign State (Informational only) | Ad Group State (Informational only) | Portfolio Name (Informational only) |
|--------|-------|-------------------------------------|-------------------------------------|-------------------------------------|
| Keyword | enabled | enabled | enabled | Portfolio_A |

**בתנאי ש-"Portfolio_A" קיים ב-Virtual Map*

### דוגמה לשורות שיסוננו:

#### סיבה: Entity לא תקין
| Entity | State | Campaign State (Informational only) | Ad Group State (Informational only) | Portfolio Name (Informational only) |
|--------|-------|-------------------------------------|-------------------------------------|-------------------------------------|
| Campaign | enabled | enabled | enabled | Portfolio_B |

#### סיבה: סטטוס לא פעיל
| Entity | State | Campaign State (Informational only) | Ad Group State (Informational only) | Portfolio Name (Informational only) |
|--------|-------|-------------------------------------|-------------------------------------|-------------------------------------|
| Keyword | paused | enabled | enabled | Portfolio_C |

#### סיבה: פורטפוליו לא קיים ב-Virtual Map (כולל מקרים של Ignore)
| Entity | State | Campaign State (Informational only) | Ad Group State (Informational only) | Portfolio Name (Informational only) |
|--------|-------|-------------------------------------|-------------------------------------|-------------------------------------|
| Keyword | enabled | enabled | enabled | Portfolio_Ignored |

**כאשר Portfolio_Ignored נמחק מה-Virtual Map בגלל סימון Ignore*

## 7. הערות
- הניקוי מתבצע **לפני** השוואת רשימות הפורטפוליוז
- לאחר הניקוי, המערכת ממשיכה לשלב השוואת הפורטפוליוז עם הנתונים המסוננים
- הניקוי לא משנה את קובץ ה-Bulk המקורי - עובד על עותק בזיכרון

### הבהרות Virtual Map (Step 2)
- רשימת ה‑Ignore נגזרת מה‑Template/Completion Templates לאחר Merge אל ה‑Virtual Map.
- השוואת הפורטפוליוז (Bulk מול Template) והפקת ה‑Completion Template הבא מתבצעות תמיד מול ה‑Virtual Map המעודכן.
- ה‑Virtual Map הוא אובייקט פנימי של Step 2 בלבד; הוא נסגר/קופא בסוף השלב ומשמש כקלט מוכן ל‑Step 3.