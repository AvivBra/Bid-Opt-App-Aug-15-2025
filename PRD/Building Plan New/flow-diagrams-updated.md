# תרשימי זרימה מעודכנים - Bid Optimizer Mockup

## תרשים זרימה ראשי - מבט על

```mermaid
flowchart TD
    Start([התחלה]) --> Upload[Step 1: Upload]
    
    Upload --> ValidateCheck{קבצים תקינים?}
    ValidateCheck -->|לא| UploadError[הודעת שגיאה]
    UploadError --> Upload
    ValidateCheck -->|כן| Validate[Step 2: Validate]
    
    Validate --> VMInit[אתחול Virtual Map]
    VMInit --> BulkClean[ניקוי Bulk]
    BulkClean --> Compare[השוואת פורטפוליוז]
    
    Compare --> Issues{יש בעיות?}
    Issues -->|לא| Freeze[VM.freeze()]
    Issues -->|חסרים| CompletionLoop[לולאת השלמה]
    Issues -->|עודפים| ShowExcess[הצגת עודפים]
    Issues -->|שניהם| BothHandle[טיפול בשניהם]
    
    CompletionLoop --> IterCheck{איטרציה < 10?}
    IterCheck -->|לא| MaxIterError[שגיאת מקסימום]
    IterCheck -->|כן| CompletionLoop
    
    CompletionLoop -->|הושלם| Freeze
    ShowExcess --> Freeze
    BothHandle --> CompletionLoop
    
    Freeze --> Output[Step 3: Output]
    Output --> CreateFiles[יצירת Working + Clean]
    CreateFiles --> Download[הורדת קבצים]
    
    Download --> Reset{New Processing?}
    Reset -->|כן| ClearAll[איפוס מלא]
    ClearAll --> Upload
    Reset -->|לא| End([סיום])
```

## Virtual Map State Machine

```mermaid
stateDiagram-v2
    [*] --> Empty: יצירה
    
    Empty --> Active: אתחול מטמפלייט
    
    Active --> Active: add_portfolio()
    Active --> Active: remove_portfolio()
    Active --> Active: merge_completion()
    
    Active --> Frozen: freeze()
    
    Frozen --> ReadOnly: ניסיון שינוי
    ReadOnly --> Frozen: נכשל
    
    Frozen --> Empty: New Processing
    
    note right of Active
        - מקבל שינויים
        - מנהל ignored list
        - מתעדכן מ-completion
    end note
    
    note right of Frozen
        - קריאה בלבד
        - get_frozen_copy()
        - משמש Step 3
    end note
```

## Completion Template Loop - מפורט

```mermaid
flowchart TD
    Start([התחלת לולאה]) --> CheckMissing{יש חסרים?}
    
    CheckMissing -->|לא| Exit([יציאה מהלולאה])
    CheckMissing -->|כן| CreateTemplate[יצירת Completion Template]
    
    CreateTemplate --> Download[הורדת קובץ למשתמש]
    Download --> UserFills[משתמש ממלא]
    
    UserFills --> Upload[העלאה חזרה]
    Upload --> Validate{ולידציה}
    
    Validate -->|שגיאות| ShowErrors[הצגת שגיאות]
    ShowErrors --> CreateTemplate
    
    Validate -->|תקין| CheckIgnore{כולם Ignore?}
    CheckIgnore -->|כן| AllIgnoreError[שגיאה: All Ignored]
    CheckIgnore -->|לא| Merge[מיזוג ל-VM]
    
    Merge --> IncrementIter[iteration++]
    IncrementIter --> CheckLimit{iteration > 10?}
    
    CheckLimit -->|כן| MaxIterError[שגיאת מקסימום]
    CheckLimit -->|לא| UpdateVM[עדכון Virtual Map]
    
    UpdateVM --> CleanBulk[ניקוי Bulk מחדש]
    CleanBulk --> Compare[השוואה מחדש]
    Compare --> CheckMissing
```

## Step 2 Service - תזמור

```mermaid
flowchart LR
    subgraph Step2Service
        Init[__init__] --> ProcessVal[process_validation]
        ProcessVal --> InitVM[initialize_virtual_map]
        InitVM --> CleanBulk[handle_bulk_cleanse]
        CleanBulk --> ComparePort[compare_portfolios]
        ComparePort --> HandleMissing[handle_missing]
        HandleMissing --> CheckIter[check_iteration]
        CheckIter --> Freeze[freeze_virtual_map]
    end
    
    subgraph Dependencies
        VM[VirtualMap]
        PC[portfolio_comparison]
        CV[completion_validator]
        BC[bulk_cleanse]
    end
    
    InitVM --> VM
    ComparePort --> PC
    HandleMissing --> CV
    CleanBulk --> BC
```

## Error Handling Flow

```mermaid
flowchart TD
    UserAction[פעולת משתמש] --> TryBlock{Try}
    
    TryBlock -->|Success| Continue[המשך]
    TryBlock -->|Error| ErrorType{סוג שגיאה}
    
    ErrorType -->|File Size| Red1[קובץ גדול מ-40MB]
    ErrorType -->|Wrong Format| Red2[לא Excel/CSV]
    ErrorType -->|Missing Headers| Red3[כותרות שגויות]
    ErrorType -->|Empty Template| Red4[טמפלייט ריק]
    ErrorType -->|All Ignored| Red5[כולם Ignore]
    ErrorType -->|Max Iterations| Red6[10 איטרציות]
    ErrorType -->|Calc Errors| Pink[Pink Notice]
    
    Red1 --> ShowError[הודעה אדומה]
    Red2 --> ShowError
    Red3 --> ShowError
    Red4 --> ShowError
    Red5 --> ShowError
    Red6 --> ShowError
    
    Pink --> ShowPink[הודעה ורודה]
    
    ShowError --> Retry[נסה שוב]
    ShowPink --> ContinueAnyway[המשך בכל זאת]
    
    Retry --> UserAction
    Continue --> End([סיום תקין])
    ContinueAnyway --> End
```

## File Generation Pipeline

```mermaid
flowchart TB
    subgraph Input
        Bulk[Bulk DataFrame]
        VM[Virtual Map - Frozen]
        Opt[Selected Optimizations]
    end
    
    subgraph Processing
        Optimizer[ZeroSalesOptimizer]
        ChangeOp[Operation → Update]
        CreateSheets[Create Sheets]
    end
    
    subgraph Output Files
        Working[Working File<br/>2 sheets]
        Clean[Clean File<br/>1 sheet]
    end
    
    Bulk --> Optimizer
    VM --> Optimizer
    Opt --> Optimizer
    
    Optimizer --> ChangeOp
    ChangeOp --> CreateSheets
    
    CreateSheets --> Working
    CreateSheets --> Clean
    
    Working --> FileName1[Auto Optimized Bulk | Working | 2025-08-15 | 14-30.xlsx]
    Clean --> FileName2[Auto Optimized Bulk | Clean | 2025-08-15 | 14-30.xlsx]
```

## Reset Flow - New Processing

```mermaid
flowchart TD
    CurrentState[מצב נוכחי] --> ClickReset[לחיצה על New Processing]
    
    ClickReset --> ClearSession[ניקוי Session State]
    
    ClearSession --> Clear1[bulk_df = None]
    ClearSession --> Clear2[template_df = None]
    ClearSession --> Clear3[virtual_map = {}]
    ClearSession --> Clear4[iteration_count = 0]
    ClearSession --> Clear5[output_files = None]
    ClearSession --> Clear6[current_step = 1]
    
    Clear1 --> RedirectUpload[הפניה ל-Upload]
    Clear2 --> RedirectUpload
    Clear3 --> RedirectUpload
    Clear4 --> RedirectUpload
    Clear5 --> RedirectUpload
    Clear6 --> RedirectUpload
    
    RedirectUpload --> FreshStart[התחלה נקייה]
```

## Data Flow Through System

```mermaid
graph LR
    subgraph Step1
        T[Template.xlsx] --> TDF[Template DF]
        B[Bulk.xlsx] --> BDF[Bulk DF]
    end
    
    subgraph Step2
        TDF --> VM[Virtual Map]
        BDF --> Clean[Cleaned Bulk]
        Clean --> Comp[Comparison]
        VM --> Comp
        Comp --> CT[Completion Template]
        CT --> VM
    end
    
    subgraph Step3
        VM --> Opt[Optimizer]
        Clean --> Opt
        Opt --> WF[Working File]
        Opt --> CF[Clean File]
    end
    
    style VM fill:#ffeb3b
    style Comp fill:#ff9800
    style Opt fill:#4caf50
```

## Iteration Counter State

```mermaid
stateDiagram-v2
    [*] --> Zero: אתחול
    Zero --> One: increment()
    One --> Two: increment()
    Two --> Three: increment()
    Three --> Four: increment()
    Four --> Five: increment()
    Five --> Six: increment()
    Six --> Seven: increment()
    Seven --> Eight: increment()
    Eight --> Nine: increment()
    Nine --> Ten: increment()
    Ten --> Error: increment()
    Error --> [*]: Reset
    
    note right of Ten
        מקסימום מותר
        הבא = שגיאה
    end note
```