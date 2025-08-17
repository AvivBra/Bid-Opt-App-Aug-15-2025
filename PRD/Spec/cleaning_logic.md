# לוגיקת הניקוי הראשוני

## שלב 1: סינון והפרדה

### מהלשונית Sponsored Products Campaigns:

**משאירים רק שורות עם:**
- Entity = Keyword
- Entity = Product Targeting  
- Entity = Product Ad
- Entity = Bidding Adjustment

**מפרידים ל-3 לשוניות:**
1. לשונית ראשית: Keyword + Product Targeting
2. לשונית נפרדת: Bidding Adjustment
3. לשונית נפרדת: Product Ad

### לשוניות נוספות:
- לשונית Portfolios - נשמרת כמו שהיא

## שלב 2: ניקוי נוסף

### מהלשוניות הבאות בלבד:
- לשונית ראשית (Keyword + Product Targeting)
- לשונית Product Ad

**מוחקים כל שורה שאינה enabled בכל 3 העמודות:**
- State
- Campaign State (Informational only)
- Ad Group State (Informational only)

### הערה:
לשוניות Bidding Adjustment & Portfolios  לא עוברות ניקוי נוסף - נשארות כמו שהן
