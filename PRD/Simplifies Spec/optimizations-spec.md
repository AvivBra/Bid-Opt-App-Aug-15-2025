# מפרט 14 אופטימיזציות - Bid Optimizer

## 1. Zero Sales Optimization

### תיאור
מוריד Bid למינימום עבור keywords/products ללא מכירות

### לוגיקה
```python
if row['Sales'] == 0 and row['Impressions'] > 100:
    row['Bid'] = template['Base Bid'] * 0.5
    if row['Bid'] < 0.02:
        row['Bid'] = 0.02
```

### שדות נדרשים
- Sales
- Impressions
- Bid

### פלט
- Bid מעודכן
- Operation = "Update"

---

## 2. Portfolio Bid Optimization

### תיאור
מתאים Bid לפי ביצועי הפורטפוליו הכולל

### לוגיקה
```python
portfolio_acos = portfolio_data['ACOS'].mean()
if portfolio_acos > target_acos * 1.2:
    row['Bid'] = row['Bid'] * 0.9
elif portfolio_acos < target_acos * 0.8:
    row['Bid'] = row['Bid'] * 1.1
```

### שדות נדרשים
- Portfolio Name
- ACOS
- Target CPA (מTemplate)

### פלט
- Bid מעודכן לכל הפורטפוליו

---

## 3. Budget Optimization

### תיאור
מתאים תקציב יומי לפי ביצועים

### לוגיקה
```python
if row['Spend'] / row['Daily Budget'] > 0.95:
    # Campaign hits budget limit
    if row['ACOS'] < target_acos:
        row['Daily Budget'] = row['Daily Budget'] * 1.2
elif row['Spend'] / row['Daily Budget'] < 0.5:
    # Under-spending
    row['Daily Budget'] = row['Daily Budget'] * 0.8
```

### שדות נדרשים
- Daily Budget
- Spend
- ACOS

### פלט
- Daily Budget מעודכן

---

## 4. Keyword Optimization

### תיאור
מתאים Bid לפי ביצועי keyword ספציפי

### לוגיקה
```python
if row['Entity'] == 'Keyword':
    keyword_ctr = row['Click-through Rate']
    if keyword_ctr > 0.5:  # High CTR
        row['Bid'] = row['Bid'] * 1.15
    elif keyword_ctr < 0.1:  # Low CTR
        row['Bid'] = row['Bid'] * 0.85
```

### שדות נדרשים
- Entity
- Click-through Rate
- Bid

### פלט
- Bid מעודכן ל-Keywords

---

## 5. Product Targeting Optimization

### תיאור
מתאים Bid למוצרים ממוקדים

### לוגיקה
```python
if row['Entity'] == 'Product Targeting':
    conversion_rate = row['Conversion Rate']
    if conversion_rate > 0.1:  # Good conversion
        row['Bid'] = row['Bid'] * 1.2
    elif conversion_rate < 0.02:  # Poor conversion
        row['Bid'] = row['Bid'] * 0.7
```

### שדות נדרשים
- Entity
- Conversion Rate
- Bid

### פלט
- Bid מעודכן ל-Product Targeting

---

## 6. Day Parting Optimization

### תיאור
מתאים Bid לפי שעות היום (סימולציה במוקאפ)

### לוגיקה
```python
# Mockup: Random assignment for demo
hour_performance = random.choice(['peak', 'normal', 'low'])
if hour_performance == 'peak':
    row['Bid'] = row['Bid'] * 1.3
elif hour_performance == 'low':
    row['Bid'] = row['Bid'] * 0.7
```

### שדות נדרשים
- Bid
- Campaign ID

### פלט
- Bid מעודכן לפי "שעות"

---

## 7. Placement Optimization

### תיאור
מתאים Bid לפי מיקום המודעה

### לוגיקה
```python
if row['Placement'] == 'Top of Search':
    row['Percentage'] = 50  # 50% increase for top
elif row['Placement'] == 'Product Pages':
    row['Percentage'] = -10  # 10% decrease
```

### שדות נדרשים
- Placement
- Percentage

### פלט
- Percentage מעודכן

---

## 8. Search Term Optimization

### תיאור
מתאים Bid לפי ביצועי מונחי חיפוש

### לוגיקה
```python
if row['Entity'] == 'Keyword':
    # Check search term performance
    if row['Orders'] > 5 and row['ACOS'] < target_acos:
        row['Bid'] = row['Bid'] * 1.25
    elif row['Orders'] == 0 and row['Clicks'] > 20:
        row['Bid'] = row['Bid'] * 0.5
```

### שדות נדרשים
- Orders
- ACOS
- Clicks

### פלט
- Bid מעודכן

---

## 9. Negative Keyword Optimization

### תיאור
מסמן keywords לא רווחיים (סימולציה)

### לוגיקה
```python
if row['Entity'] == 'Keyword':
    if row['Spend'] > 10 and row['Sales'] == 0:
        # Mark for negative (in real version)
        row['State'] = 'paused'  # Mockup action
```

### שדות נדרשים
- Spend
- Sales
- State

### פלט
- State = "paused" לגרועים

---

## 10. ASIN Targeting Optimization

### תיאור
מתאים Bid למוצרים ספציפיים

### לוגיקה
```python
if row['ASIN'] and row['Entity'] == 'Product Targeting':
    asin_performance = row['ROAS']
    if asin_performance > 3:  # Good ROAS
        row['Bid'] = row['Bid'] * 1.3
    elif asin_performance < 1:  # Poor ROAS
        row['Bid'] = row['Bid'] * 0.6
```

### שדות נדרשים
- ASIN
- ROAS
- Bid

### פלט
- Bid מעודכן לפי ASIN

---

## 11. Category Targeting Optimization

### תיאור
מתאים Bid לקטגוריות מוצרים

### לוגיקה
```python
if 'category' in row['Product Targeting Expression'].lower():
    category_ctr = row['Click-through Rate']
    if category_ctr > 0.3:
        row['Bid'] = row['Bid'] * 1.2
    else:
        row['Bid'] = row['Bid'] * 0.9
```

### שדות נדרשים
- Product Targeting Expression
- Click-through Rate

### פלט
- Bid מעודכן לקטגוריות

---

## 12. Budget Allocation Optimization

### תיאור
מחלק תקציב בין campaigns

### לוגיקה
```python
# Calculate total budget
total_budget = campaigns['Daily Budget'].sum()
# Redistribute based on performance
for campaign in campaigns:
    performance_score = campaign['ROAS'] / campaign['ACOS']
    campaign['Daily Budget'] = total_budget * performance_score
```

### שדות נדרשים
- Daily Budget
- ROAS
- ACOS

### פלט
- Daily Budget מחולק מחדש

---

## 13. Campaign Structure Optimization

### תיאור
ממליץ על שינויי מבנה (סימולציה)

### לוגיקה
```python
# Check campaign structure issues
ad_groups_count = df['Ad Group ID'].nunique()
if ad_groups_count > 20:
    # Flag for restructuring
    row['Operation'] = 'Update'  # Mockup action
```

### שדות נדרשים
- Campaign ID
- Ad Group ID

### פלט
- Operation flags

---

## 14. Bid Modifier Optimization

### תיאור
מתאים מכפילי Bid

### לוגיקה
```python
# Apply bid modifiers based on device/location (mockup)
base_bid = row['Bid']
modifiers = {
    'mobile': 0.9,
    'desktop': 1.1,
    'tablet': 1.0
}
# Mockup: random device
device = random.choice(['mobile', 'desktop', 'tablet'])
row['Bid'] = base_bid * modifiers[device]
```

### שדות נדרשים
- Bid

### פלט
- Bid עם modifiers

---

## סיכום טכני

### כללים לכל האופטימיזציות
1. **Bid Range:** 0.02 - 1.25 (מינימום-מקסימום)
2. **Budget Minimum:** 1.00
3. **Operation:** תמיד "Update"
4. **Error Handling:** דלג על שורות עם ערכים חסרים

### סדר ביצוע
```python
optimization_order = [
    'Zero Sales',           # First - remove waste
    'Portfolio Bid',        # Portfolio level
    'Budget Optimization',  # Campaign level
    'Keyword Optimization', # Entity level
    'Product Targeting',    # Entity level
    'Day Parting',         # Time based
    'Placement',           # Position based
    'Search Term',         # Query level
    'Negative Keyword',    # Exclusions
    'ASIN Targeting',      # Product specific
    'Category Targeting',  # Category level
    'Budget Allocation',   # Redistribution
    'Campaign Structure',  # Structure
    'Bid Modifier'        # Final adjustments
]
```

### Conflict Resolution
אם מספר אופטימיזציות משנות את אותו השדה:
- האחרונה בסדר מנצחת
- ערך מקסימלי/מינימלי נשמר