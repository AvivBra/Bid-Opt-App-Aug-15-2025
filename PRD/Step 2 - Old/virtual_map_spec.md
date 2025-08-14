# Virtual Map Specification - איפיון טכני מלא

## Overview
The Virtual Map is the central data structure that bridges Step 2 and Step 3.

## מבנה נתונים

```python
class VirtualMap:
    def __init__(self):
        self.data = {}  # {portfolio_name: {base_bid, target_cpa, is_ignored}}
        self.is_frozen = False
        self.frozen_copy = None
```

### מבנה Entry
```python
{
    "portfolio_name": {
        "base_bid": float,
        "target_cpa": float | None,
        "is_ignored": bool
    }
}
```

## כללי מיזוג (Merge Rules)

### 1. דריסה מלאה
- **כלל**: ערכים חדשים מ-Completion Template דורסים ערכים קיימים
- **דוגמה**: אם Portfolio_A קיים עם base_bid=1.5 וב-Completion מגיע עם base_bid=2.0, הערך יעודכן ל-2.0

### 2. טיפול ב-Ignore
- **בטמפלט ראשוני**: פורטפוליו עם Base Bid="Ignore" לא נכנס ל-Virtual Map כלל
- **בטמפלט השלמה**: אם מופיע Base Bid="Ignore", הפורטפוליו יימחק מה-Virtual Map
- **השפעה על ניקוי**: כל השורות ב-Bulk עם פורטפוליו שמסומן Ignore יוסרו בניקוי הראשוני

### 3. שמירת מידע קיים
- פורטפוליוז שלא מופיעים ב-Completion Template נשארים ללא שינוי
- רק פורטפוליוז המופיעים ב-Completion מתעדכנים/נדרסים

## ולידציות במיזוג

### שגיאות חוסמות (מחזירות למילוי מחדש)
| בעיה | הודעת שגיאה | פעולה |
|------|-------------|--------|
| Base Bid חסר | "Base Bid is required for portfolio: {name}" | חזרה למילוי Completion Template |
| Base Bid לא תקין | "Invalid Base Bid value for portfolio: {name}" | חזרה למילוי Completion Template |
| Target CPA לא תקין | "Invalid Target CPA value for portfolio: {name}" | הצגת שגיאה וחזרה למילוי |
| Portfolio לא קיים ב-Bulk | "Portfolio '{name}' does not exist in Bulk file" | הצגת שגיאה עם שם הפורטפוליו |

## States

### Active State (Step 2)
- Accepts new data from Completion Templates
- Merges portfolios dynamically with full override
- Can be modified through user uploads
- Portfolios with "Ignore" are removed from map

### Frozen State (Step 3)
- Read-only snapshot of final Step 2 data
- Used for all optimization calculations
- Cannot be modified without returning to Step 2

## State Transitions

| From | To | Trigger | Action |
|------|-----|---------|--------|
| Active | Active | Upload Completion | Merge with override |
| Active | Frozen | User clicks Continue | Deep copy + lock |
| Frozen | Active | User returns to Step 2 | Unlock for editing |

## Implementation Functions

```python
class VirtualMapManager:
    def initialize_from_template(self, template_df):
        """טעינה ראשונית מטמפלט"""
        for _, row in template_df.iterrows():
            if row['Base Bid'] != "Ignore":
                self.data[row['Portfolio Name']] = {
                    'base_bid': row['Base Bid'],
                    'target_cpa': row.get('Target CPA'),
                    'is_ignored': False
                }
    
    def merge_completion_template(self, completion_df):
        """מיזוג עם דריסה מלאה"""
        for _, row in completion_df.iterrows():
            portfolio = row['Portfolio Name']
            
            # בדיקת קיום ב-Bulk
            if not self.portfolio_exists_in_bulk(portfolio):
                raise ValueError(f"Portfolio '{portfolio}' does not exist in Bulk file")
            
            # טיפול ב-Ignore
            if row['Base Bid'] == "Ignore":
                if portfolio in self.data:
                    del self.data[portfolio]
            else:
                # דריסה מלאה או הוספה חדשה
                self.data[portfolio] = {
                    'base_bid': row['Base Bid'],
                    'target_cpa': row.get('Target CPA'),
                    'is_ignored': False
                }
    
    def get_missing_portfolios(self, bulk_portfolios):
        """מחזיר רשימת פורטפוליוז חסרים"""
        vm_portfolios = set(self.data.keys())
        return list(set(bulk_portfolios) - vm_portfolios)
    
    def freeze(self):
        """נעילה במעבר ל-Step 3"""
        self.is_frozen = True
        self.frozen_copy = deepcopy(self.data)
    
    def unfreeze(self):
        """שחרור נעילה בחזרה ל-Step 2"""
        self.is_frozen = False
```

## השפעה על ניקוי ראשוני

בזמן הניקוי הראשוני ב-Step 2, המערכת:
1. בודקת את ה-Virtual Map הנוכחי
2. מסננת החוצה כל שורה ב-Bulk שה-Portfolio Name שלה לא קיים ב-Virtual Map
3. זה כולל פורטפוליוז שנמחקו בגלל "Ignore"

## דוגמאות

### דוגמה 1: דריסת ערכים
```
# Virtual Map לפני:
{"Portfolio_A": {"base_bid": 1.5, "target_cpa": 3.0}}

# Completion Template:
Portfolio_A | 2.0 | 4.0

# Virtual Map אחרי:
{"Portfolio_A": {"base_bid": 2.0, "target_cpa": 4.0}}
```

### דוגמה 2: מחיקה עם Ignore
```
# Virtual Map לפני:
{"Portfolio_B": {"base_bid": 1.5, "target_cpa": None}}

# Completion Template:
Portfolio_B | Ignore | 

# Virtual Map אחרי:
{} # Portfolio_B נמחק
```