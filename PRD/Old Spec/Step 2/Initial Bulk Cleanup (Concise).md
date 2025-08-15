# ניקוי ראשוני של Bulk File - מפרט תמציתי

## מטרה
סינון שורות לא רלוונטיות מה-Bulk לפני השוואת פורטפוליוז.

## קלט
- Bulk DataFrame (לשונית Sponsored Products Campaigns)
- רשימת ignored_portfolios מה-Virtual Map

## תנאי סינון
שורה נשמרת **רק אם כל התנאים מתקיימים**:

### 1. Entity
- ערך נדרש: "Product Targeting" או "Keyword"

### 2. State
- ערך נדרש: "enabled"

### 3. Campaign State (Informational only)
- ערך נדרש: "enabled"

### 4. Ad Group State (Informational only)
- ערך נדרש: "enabled"

### 5. Portfolio Name (Informational only)
- ערך נדרש: **לא** ברשימת ignored
- **השוואה case-sensitive** - "Portfolio_A" ≠ "portfolio_a"

## פלט
DataFrame מנוקה עם שורות רלוונטיות בלבד

## דוגמה

| Entity | State | Campaign State | Ad Group State | Portfolio Name (Informational only) | נשמר? |
|--------|-------|----------------|----------------|-------------------------------------|-------|
| Keyword | enabled | enabled | enabled | Port_A | ✓ |
| Campaign | enabled | enabled | enabled | Port_B | ✗ (Entity) |
| Keyword | paused | enabled | enabled | Port_C | ✗ (State) |
| Keyword | enabled | enabled | enabled | Port_Ignored | ✗ (Ignored) |

## טיפול במקרי קצה
- אם לא נשארו שורות → שגיאה: "After first cleanse no rows are left in bulk file - go back to step 1"
- אם אין לשונית Sponsored Products Campaigns → שגיאה: "Bulk file lacks 'Sponsored Products Campaigns' - reupload in step 1"

## הערות
- מתבצע **לפני** השוואת פורטפוליוז
- **חשוב**: אם המשתמש מעלה קובץ חדש בסטפ 1, כל התהליך מתאפס והוא צריך להתחיל מחדש