# מפרט UI/UX - Bid Optimizer

## 1. עקרונות עיצוב

### Visual Design
- **צבע ראשי:** אדום (#FF0000) לכפתורים ראשיים
- **רקע:** לבן (#FFFFFF)
- **טקסט:** שחור (#000000)
- **ללא אימוג'י או אייקונים**
- **גופן:** Arial/Helvetica (ברירת מחדל של הדפדפן)

### Layout
- **עמוד יחיד** עם גלילה אנכית
- **רוחב:** Responsive, מקסימום 1200px
- **מרווחים:** 20px בין סעיפים
- **יישור:** מרכז

## 2. מבנה העמוד

```
┌─────────────────────────────────────┐
│         Bid Optimizer - Bulk File    │
│              ─────────────           │
├─────────────────────────────────────┤
│                                     │
│  ┌─── Upload Section ──────────┐   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─── Validation Section ──────┐   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─── Output Section ──────────┐   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

## 3. Upload Section

### מצב התחלתי
```
Upload Files
────────────

[Download Template]  <- כפתור אדום

Template File:
[Drop file here or browse]  <- אזור אפור

Bulk File:
[Drop file here or browse]  <- אזור אפור

Select Optimizations:
☐ Zero Sales
☐ Portfolio Bid Optimization
☐ Budget Optimization
[... 11 more]
```

### מצב אחרי העלאה
```
Upload Files
────────────

[Download Template]

Template File: ✓ template.xlsx (125 KB)
Bulk File: ✓ bulk.xlsx (2.3 MB)

Select Optimizations:
☑ Zero Sales
☐ Portfolio Bid Optimization
[... 12 more]
```

## 4. Validation Section

### מצב התחלתי (ריק)
```
Validation Results
──────────────────
[אזור ריק - מוסתר]
```

### מצב תקין
```
Validation Results
──────────────────
✓ All portfolios valid
All portfolios in Bulk file have Base Bid values in Template

[Process Files]  <- כפתור אדום פעיל
```

### מצב חסרים
```
Validation Results
──────────────────
❌ Missing portfolios found

The following portfolios are in Bulk but not in Template:
• Portfolio_ABC
• Portfolio_DEF
• Portfolio_GHI

[Upload New Template]  <- כפתור אדום
```

### מצב עיבוד
```
Validation Results
──────────────────
Validating...
[=====>          ] 35%
```

## 5. Output Section

### מצב התחלתי (ריק)
```
Output Files
────────────
[אזור ריק - מוסתר]
```

### מצב עיבוד
```
Output Files
────────────
Processing optimizations...
[=========>      ] 65%
```

### מצב מוכן
```
Output Files
────────────
✓ Processing complete

Files generated:
• Working File: 2.4 MB (14 sheets)
• Clean File: 1.8 MB (7 sheets)

[Download Working File]  <- כפתור אדום
[Download Clean File]    <- כפתור אדום
[Reset]                  <- כפתור אפור
```

### Pink Notice (שגיאות חישוב)
```
Output Files
────────────
✓ Processing complete

┌─────────────────────────────────────┐
│ Please note: 7 calculation errors   │
│ in Zero Sales optimization          │
└─────────────────────────────────────┘
   <- רקע ורוד (#FFE4E1)

Files generated:
[...]
```

## 6. הודעות

### Error (אדום)
```
┌─────────────────────────────────────┐
│ ❌ File exceeds 40MB limit          │
└─────────────────────────────────────┘
```

### Warning (כתום)
```
┌─────────────────────────────────────┐
│ ⚠️ 15 rows have invalid Bid values  │
└─────────────────────────────────────┘
```

### Info (כחול)
```
┌─────────────────────────────────────┐
│ ℹ️ Processing 10,000 rows...        │
└─────────────────────────────────────┘
```

### Success (ירוק)
```
┌─────────────────────────────────────┐
│ ✓ Files uploaded successfully       │
└─────────────────────────────────────┘
```

## 7. כפתורים

### Primary (אדום)
```
[Download Template]
[Process Files]
[Upload New Template]
[Download Working File]
[Download Clean File]
```

### Secondary (אפור)
```
[Reset]
[Cancel]
```

### מצבי כפתורים
- **פעיל:** צבע מלא, cursor pointer
- **לא פעיל:** צבע דהוי, cursor not-allowed
- **Loading:** אנימציית spinner

## 8. Responsive Behavior

### Desktop (>1024px)
- פריסה מלאה
- כל הרכיבים זה מתחת לזה

### Tablet (768-1024px)
- פריסה מותאמת
- כפתורים ברוחב מלא

### Mobile (<768px)
- לא נתמך
- הודעה: "Please use desktop browser"

## 9. Animations

### Progress Bar
```
[=====>          ] 35%
מתעדכן כל 500ms
```

### File Upload
```
Drag & Drop: הדגשת גבול כחול
Upload: Progress indicator
Complete: Fade in של ✓
```

### Transitions
- הודעות: Fade in/out (300ms)
- כפתורים: Color transition (200ms)
- Sections: Slide down (400ms)

## 10. מצבי אפליקציה

### State Machine
```
INITIAL
  ↓
UPLOADING
  ↓
VALIDATING
  ↓
READY_TO_PROCESS / NEED_FIX
  ↓           ↓
PROCESSING   UPLOADING
  ↓
COMPLETE
  ↓
INITIAL (Reset)
```

### מה מוצג בכל מצב

| State | Upload | Validation | Output |
|-------|--------|------------|--------|
| INITIAL | פעיל | מוסתר | מוסתר |
| UPLOADING | פעיל | מוסתר | מוסתר |
| VALIDATING | disabled | טוען | מוסתר |
| READY_TO_PROCESS | disabled | תקין | מוסתר |
| NEED_FIX | פעיל | שגיאה | מוסתר |
| PROCESSING | disabled | disabled | טוען |
| COMPLETE | disabled | disabled | פעיל |

## 11. Accessibility

### Keyboard Navigation
- Tab order לוגי
- Enter לאישור
- Escape לביטול

### Screen Readers
- ARIA labels על כל הכפתורים
- Role attributes
- Alt text לאייקונים (אם יהיו)

### Contrast
- טקסט: 7:1 ratio
- כפתורים: 4.5:1 ratio
- שגיאות: אדום כהה (#CC0000)