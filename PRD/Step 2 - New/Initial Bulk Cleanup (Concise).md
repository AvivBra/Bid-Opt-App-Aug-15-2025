# ניקוי ראשוני של Bulk File - מפרט תמציתי

## מטרה
סינון שורות לא רלוונטיות מה-Bulk לפני השוואת פורטפוליוז.

## קלט
- Bulk DataFrame (לשונית Sponsored Products Campaigns)
- רשימת ignored_portfolios מה-Virtual Map

## תנאי סינון
שורה נשמרת **רק אם כל התנאים מתקיימים**:

| תנאי | ערך נדרש |
|------|-----------|
| Entity | "Product Targeting" או "Keyword" |
| State | "enabled" |
| Campaign State (Informational only) | "enabled" |
| Ad Group State (Informational only) | "enabled" |
| Portfolio Name (Informational only) | **לא** ברשימת ignored |

## פלט
DataFrame מנוקה עם שורות רלוונטיות בלבד

## דוגמה

| Entity | State | Campaign State | Ad Group State | Portfolio | נשמר? |
|--------|-------|----------------|----------------|-----------|-------|
| Keyword | enabled | enabled | enabled | Port_A | ✓ |
| Campaign | enabled | enabled | enabled | Port_B | ✗ (Entity) |
| Keyword | paused | enabled | enabled | Port_C | ✗ (State) |
| Keyword | enabled | enabled | enabled | Port_Ignored | ✗ (Ignored) |

## טיפול במקרי קצה
- אם לא נשארו שורות → שגיאה: "After first cleanse no rows are left in bulk file"
- אם אין לשונית Sponsored Products Campaigns → שגיאה

## הערות
- הניקוי **לא מסנן** לפי Virtual Map, רק לפי ignored
- מתבצע **לפני** השוואת פורטפוליוז