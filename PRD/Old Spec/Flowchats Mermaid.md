# Flowcharts – Mermaid Diagrams

המסמך מציג תרשימי זרימה גרפיים (Mermaid) לכל התרחישים: שלבים 1–3, ולתרחישי השגיאה/הודעות.

> הערה: התרשימים מתיישרים לדרישות ה־UI המעודכן עם סרגל צד, מעבר אחורה תמידי, ומעבר קדימה רק לאחר עמידה בדרישות השלב.

---

## Step 1 – Upload (Main Flow)

```mermaid
flowchart TD
  A([Start]) --> B[Upload Bulk + Template + Checklist]
  B --> C{Validation Pass?}
  C -- Yes --> D[Enable Step 2 Navigation]
  C -- No --> E[Show Relevant Error]
  E --> B
```

## Step 2 – Validate Portfolios (Main Flow)

```mermaid
flowchart TD
  A2([Start Step 2]) --> B2[Compare Portfolios]
  B2 --> C2{Scenario?}
  C2 -- Missing only --> D2[Show Download Completion Template]
  D2 --> E2[Loop Until All Missing Filled]
  E2 --> F2[Go to Step 3]

  C2 -- Excess only --> G2[Show Excess List + Copy Button]
  G2 --> H2[Show Continue Button]
  H2 --> F2

  C2 -- Missing & Excess --> I2[Show Download Template + Excess List + Copy Button + Disabled Continue Button]
  I2 --> J2[Loop Until Missing Filled]
  J2 --> H2[Enable Continue Button]
```

## Step 3 – Optimization & Output (Main Flow)

```mermaid
flowchart TD
  A3([Start Step 3]) --> B3[Generate Working + Clean Files]
  B3 --> C3[Show 3 Buttons: Download Working, Download Clean, New Processing]
  C3 -->|Download Working| D3[Stay on Same Screen]
  C3 -->|Download Clean| D3
  C3 -->|New Processing| E3[Reset All Data]
  E3 --> F3[Go to Step 1]
```

---

## Step 1 – Error Flow

```mermaid
flowchart TD
  U1[Upload Files]
  U1 --> A1{Wrong Titles?}
  A1 -- Yes --> E1[Show Wrong Title Error]
  E1 --> U1
  A1 -- No --> B1{File Too Big?}
  B1 -- Yes --> E2[Show Size Error]
  E2 --> U1
  B1 -- No --> C1{Wrong Format?}
  C1 -- Yes --> E3[Show Format Error]
  E3 --> U1
  C1 -- No --> D1{Missing Files OR No Optimization Selected?}
  D1 -- Yes --> E4[Disable Step 2 + Wait]
  E4 --> U1
  D1 -- No --> F1[Enable Step 2]
```

## Step 2 – Error Flow

```mermaid
flowchart TD
  V1[Upload Template]
  V1 --> A2{Wrong Titles?}
  A2 -- Yes --> X1[Show Titles Error]
  X1 --> V1
  A2 -- No --> B2{Empty Template?}
  B2 -- Yes --> X2[Show Empty Template Error]
  X2 --> V1
  B2 -- No --> C2{All Ignore?}
  C2 -- Yes --> X3[Show All Ignore Error (Stop)]
  C2 -- No --> D2{Wrong Format?}
  D2 -- Yes --> X4[Show Format Error]
  X4 --> V1
  D2 -- No --> E2[Proceed per Scenario]
```

## Step 3 – Info Messages Flow (Non-Blocking)

```mermaid
flowchart TD
  W1[After Optimization]
  W1 --> A3{Calculation Errors?}
  A3 -- Yes --> Y1[Show Error Count per Sheet]
  A3 -- No --> B3{Out-of-Range Bids?}
  B3 -- Yes --> Y2[Show Above 1.25 Count + Below 0.02 Count]
  B3 -- No --> Z3[Ready to Download]
```

---

## Sidebar Navigation Logic (Global)

```mermaid
flowchart TD
  S1[Sidebar]
  S1 --> S2[Can always navigate backward]
  S1 --> S3{Forward step allowed?}
  S3 -- Only if step requirements met --> S4[Enable forward navigation]
  S3 -- Otherwise --> S5[Disable forward navigation]
```

---

## Notes

* לחיצה על **New Processing** בשלב 3 מאפסת נתונים, מחזירה ל־Step 1, וחוסמת מעבר קדימה עד עמידה מחדש בדרישות.
* ב־Step 2, לחיצה על **Copy to Clipboard** לרשימת העודפים **אינה** משנה מסך ואינה מעבירה לשלב הבא.
* ב־Step 2, כפתור **Continue** קיים מיידית בתרחיש "עודפים בלבד", אך בתרחיש "חוסרים ועודפים" יופיע רק לאחר מילוי החוסרים.
