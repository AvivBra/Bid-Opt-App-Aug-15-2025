# מפרט פונקציות - Bid Optimizer

## 1. Orchestrator Service

### תפקיד
מתאם ראשי בין כל השכבות

### פונקציות עיקריות

```python
class Orchestrator:
    
    def process_upload(self, 
                      template_file: BytesIO, 
                      bulk_file: BytesIO) -> Dict[str, Any]:
        """
        מעבד קבצים שהועלו
        Returns: {
            'template_df': pd.DataFrame,
            'bulk_df': pd.DataFrame,
            'success': bool,
            'errors': List[str]
        }
        """
    
    def validate_files(self, 
                      template_df: pd.DataFrame, 
                      bulk_df: pd.DataFrame) -> ValidationResult:
        """
        מבצע ולידציה מלאה
        Returns: ValidationResult object
        """
    
    def run_optimizations(self,
                         bulk_df: pd.DataFrame,
                         template_df: pd.DataFrame,
                         selected: List[str]) -> Dict[str, pd.DataFrame]:
        """
        מריץ אופטימיזציות נבחרות
        Returns: {
            'working_sheets': Dict[str, pd.DataFrame],
            'clean_sheets': Dict[str, pd.DataFrame]
        }
        """
    
    def generate_output_files(self,
                             sheets: Dict[str, pd.DataFrame]) -> Dict[str, BytesIO]:
        """
        יוצר קבצי Excel
        Returns: {
            'working_file': BytesIO,
            'clean_file': BytesIO
        }
        """
```

## 2. Base Optimization Class

### תפקיד
מחלקת בסיס לכל האופטימיזציות

```python
from abc import ABC, abstractmethod

class BaseOptimization(ABC):
    
    @property
    @abstractmethod
    def name(self) -> str:
        """שם האופטימיזציה"""
        pass
    
    @abstractmethod
    def optimize(self, 
                df: pd.DataFrame, 
                template_df: pd.DataFrame) -> pd.DataFrame:
        """
        מבצע אופטימיזציה
        Args:
            df: Bulk DataFrame
            template_df: Template DataFrame
        Returns:
            DataFrame מעודכן
        """
        pass
    
    @abstractmethod
    def validate_input(self, df: pd.DataFrame) -> bool:
        """
        בודק תקינות קלט
        Returns: True אם תקין
        """
        pass
    
    def get_statistics(self, 
                      original_df: pd.DataFrame,
                      optimized_df: pd.DataFrame) -> Dict[str, Any]:
        """
        מחשב סטטיסטיקות
        Returns: {
            'rows_modified': int,
            'bid_changes': int,
            'errors': int
        }
        """
        pass
```

## 3. Validators

### Template Validator

```python
class TemplateValidator:
    
    def validate(self, df: pd.DataFrame) -> ValidationResult:
        """
        בודק תקינות Template
        Returns: ValidationResult
        """
    
    def check_columns(self, df: pd.DataFrame) -> bool:
        """
        בודק נוכחות עמודות נדרשות
        """
    
    def check_base_bids(self, df: pd.DataFrame) -> List[str]:
        """
        בודק ערכי Base Bid
        Returns: רשימת שגיאות
        """
    
    def check_portfolios(self, df: pd.DataFrame) -> List[str]:
        """
        בודק שמות פורטפוליוז
        Returns: רשימת כפילויות
        """
```

### Bulk Validator

```python
class BulkValidator:
    
    def validate(self, df: pd.DataFrame) -> ValidationResult:
        """
        בודק תקינות Bulk
        """
    
    def check_required_sheet(self, file: BytesIO) -> bool:
        """
        בודק נוכחות Sheet נדרש
        """
    
    def clean_bulk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        מנקה Bulk:
        - Entity = Keyword/Product Targeting
        - State = enabled
        Returns: DataFrame מנוקה
        """
    
    def extract_portfolios(self, df: pd.DataFrame) -> List[str]:
        """
        מחלץ רשימת פורטפוליוז
        """
```

## 4. File Readers

### Excel Reader

```python
class ExcelReader:
    
    def read(self, 
            file: BytesIO, 
            sheet_name: str = None) -> pd.DataFrame:
        """
        קורא קובץ Excel
        Args:
            file: קובץ בזיכרון
            sheet_name: שם Sheet (אופציונלי)
        Returns: DataFrame
        Raises: 
            FileReadError: אם הקריאה נכשלה
            SheetNotFoundError: אם Sheet לא קיים
        """
    
    def get_sheet_names(self, file: BytesIO) -> List[str]:
        """
        מחזיר רשימת Sheets
        """
    
    def validate_size(self, file: BytesIO) -> bool:
        """
        בודק גודל קובץ
        Returns: True אם < 40MB
        """
```

### CSV Reader

```python
class CSVReader:
    
    def read(self, file: BytesIO) -> pd.DataFrame:
        """
        קורא קובץ CSV
        """
    
    def detect_encoding(self, file: BytesIO) -> str:
        """
        מזהה encoding
        Returns: 'utf-8' או 'windows-1252'
        """
```

## 5. Output Writer

```python
class OutputWriter:
    
    def create_excel(self,
                    sheets: Dict[str, pd.DataFrame],
                    filename: str) -> BytesIO:
        """
        יוצר קובץ Excel עם מספר Sheets
        Args:
            sheets: {sheet_name: DataFrame}
            filename: שם הקובץ
        Returns: קובץ בזיכרון
        """
    
    def format_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        מעצב עמודות:
        - IDs כטקסט
        - מספרים עם 3 ספרות אחרי הנקודה
        """
    
    def generate_filename(self, 
                         file_type: str,
                         timestamp: datetime = None) -> str:
        """
        יוצר שם קובץ
        Format: Auto Optimized Bulk | {type} | YYYY-MM-DD | HH-MM
        """
```

## 6. File Generator

```python
class FileGenerator:
    
    def generate_working_file(self,
                             optimized_data: Dict[str, pd.DataFrame]) -> BytesIO:
        """
        יוצר Working File
        כולל Clean + Working sheets
        """
    
    def generate_clean_file(self,
                           optimized_data: Dict[str, pd.DataFrame]) -> BytesIO:
        """
        יוצר Clean File
        רק Clean sheets
        """
    
    def add_operation_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        מוסיף/מעדכן עמודת Operation = "Update"
        """
```

## 7. Data Models

### Portfolio Model

```python
@dataclass
class Portfolio:
    name: str
    base_bid: float
    target_cpa: Optional[float] = None
    is_ignored: bool = False
    
    def validate(self) -> bool:
        """בודק תקינות"""
        return self.base_bid >= 0
```

### ValidationResult Model

```python
@dataclass
class ValidationResult:
    is_valid: bool
    missing_portfolios: List[str]
    excess_portfolios: List[str]
    errors: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """ממיר ל-dictionary"""
    
    def get_message(self) -> str:
        """יוצר הודעה למשתמש"""
```

## 8. Session State Manager

```python
class SessionStateManager:
    
    def initialize(self):
        """אתחול State"""
    
    def set(self, key: str, value: Any):
        """שמירת ערך"""
    
    def get(self, key: str, default: Any = None) -> Any:
        """קריאת ערך"""
    
    def clear(self):
        """איפוס מלא"""
    
    def get_current_state(self) -> str:
        """מחזיר מצב נוכחי: upload/validate/process/complete"""
    
    def can_proceed(self) -> bool:
        """בודק אם ניתן להמשיך לשלב הבא"""
```

## 9. חתימות אופטימיזציות

כל אופטימיזציה יורשת מ-BaseOptimization ומממשת:

```python
class ZeroSales(BaseOptimization):
    name = "Zero Sales"
    
    def optimize(self, df, template_df):
        # לוגיקה ספציפית
        
class PortfolioBid(BaseOptimization):
    name = "Portfolio Bid"
    
    def optimize(self, df, template_df):
        # לוגיקה ספציפית
        
# וכך הלאה ל-14 האופטימיזציות
```