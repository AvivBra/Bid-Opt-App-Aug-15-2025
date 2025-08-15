
### Zero Sales Optimization

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

