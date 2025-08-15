# רשימת פונקציות חסרות - גרסה ממוקדת

## סיכום: 35 פונקציות קריטיות בלבד (במקום 150)

## עדיפות קריטית - יום 1 (10 פונקציות)

### core/mapping/virtual_map.py
```python
1. __init__()                    # אתחול המפה
2. add_portfolio()                # הוספת פורטפוליו
3. freeze()                       # נעילה לסטפ 3
4. unfreeze()                     # ביטול נעילה (אם בכלל)
5. is_frozen()                    # בדיקת סטטוס
6. get_frozen_copy()              # קבלת עותק קפוא
7. merge_completion_template()    # מיזוג קומפלישן
```

### core/validate/portfolio_comparison.py
```python
8. compare_portfolios()           # השוואה ראשית
9. get_missing_portfolios()       # מציאת חסרים
10. get_excess_portfolios()       # מציאת עודפים
```

## עדיפות גבוהה - יום 2 (8 פונקציות)

### services/step2_service.py
```python
11. __init__()                    # אתחול עם וירטואל מאפ
12. process_validation()          # תזמור ראשי
13. handle_missing_portfolios()   # טיפול בחסרים
14. check_iteration_limit()       # בדיקת מגבלת 10
15. increment_iteration()         # הגדלת מונה
```

### core/validate/completion_validator.py
```python
16. validate_completion_template() # ולידציה ראשית
17. check_base_bid_values()       # בדיקת בייס ביד
18. check_all_ignored()           # בדיקה שלא כולם איגנור
```

## עדיפות בינונית - יום 3 (7 פונקציות)

### app/ui/tabs/validate_tab.py (ריפקטור)
```python
19. render()                      # פונקציה ראשית נקייה
20. show_missing_section()        # הצגת חסרים
21. show_excess_section()         # הצגת עודפים
22. handle_completion_upload()    # טיפול בהעלאה
```

### app/ui/messages.py (עדכון)
```python
23. show_pink_notice()            # הודעה ורודה
24. show_iteration_count()        # הצגת מונה
```

### app/state/session.py (עדכון)
```python
25. increment_iteration_counter() # הגדלת מונה
```

## עדיפות רגילה - יום 4 (10 פונקציות)

### core/output/files_builder.py
```python
26. generate_output_filename()    # שמות דינמיים
27. create_working_file()         # יצירת וורקינג
28. create_clean_file()           # יצירת קלין
```

### optimizers/zero_sales/optimizer.py
```python
29. optimize()                    # אופטימיזציה (מוקאפ)
30. create_sheets()               # יצירת שיטס
31. change_operation_to_update()  # שינוי לאפדייט
```

### optimizers/zero_sales/processors/sheet_creator.py
```python
32. create_clean_sheet()          # יצירת שיט נקי
33. create_working_sheet()        # יצירת שיט עבודה
```

### app/ui/tabs/output_tab.py
```python
34. process_optimizations()       # עיבוד אופטימיזציות
35. show_download_buttons()       # הצגת כפתורי הורדה
```

## פונקציות שבוטלו (לא נדרשות למוקאפ)

### לא קריטיות - ניתן לוותר
- כל הפונקציות בutils/debug_manager
- כל הפונקציות בutils/format_utils  
- models/file_schemas - כבר עובד עם הקיים
- services/portfolio_service - מיותר
- 14 סוגי אופטימיזציות נוספים - לא במוקאפ

### כבר קיימות ועובדות
- validate_file_size() - קיים
- validate_file_format() - קיים
- check_column_headers() - קיים

## מיפוי לימי עבודה

| יום | פונקציות | קבצים | שעות |
|-----|-----------|--------|-------|
| 1 | 10 | virtual_map, portfolio_comparison | 6 |
| 2 | 8 | step2_service, completion_validator | 6 |
| 3 | 7 | validate_tab refactor, messages | 5 |
| 4 | 10 | files_builder, optimizer | 6 |
| 5 | 0 | בדיקות בלבד | 4 |

## הערות

1. **כל פונקציה חייבת טסט** - לא ממשיכים בלי
2. **Quick Wins קודם** - iteration_count, pink notice
3. **מוקאפ בלבד** - לא צריך חישובים אמיתיים
4. **פשוט עובד** - לא צריך להיות מושלם

## Definition of Done לכל פונקציה

- [ ] הפונקציה כתובה
- [ ] יש לה טסט שעובר
- [ ] נבדקה בממשק
- [ ] אין שגיאות אימפורט