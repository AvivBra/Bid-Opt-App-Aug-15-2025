# מפרט טיפול בשגיאות - Bid Optimizer

## 1. היררכיית Exceptions

### Base Exception
```python
class BidOptimizerError(Exception):
    """Base exception for all app errors"""
    code: str
    message: str
    user_message: str
```

### File Errors
```python
class FileError(BidOptimizerError):
    """Base for file-related errors"""

class FileSizeError(FileError):
    code = "FILE_001"
    message = "File exceeds size limit"
    user_message = "File must be smaller than 40MB"

class FileFormatError(FileError):
    code = "FILE_002"
    message = "Invalid file format"
    user_message = "File must be Excel (.xlsx) or CSV"

class FileReadError(FileError):
    code = "FILE_003"
    message = "Cannot read file"
    user_message = "Unable to read the file. Please check it's not corrupted"

class SheetNotFoundError(FileError):
    code = "FILE_004"
    message = "Required sheet not found"
    user_message = "Sheet 'Sponsored Products Campaigns' not found in Bulk file"
```

### Validation Errors
```python
class ValidationError(BidOptimizerError):
    """Base for validation errors"""

class MissingColumnsError(ValidationError):
    code = "VAL_001"
    message = "Required columns missing"
    user_message = "Missing required columns: {columns}"

class EmptyFileError(ValidationError):
    code = "VAL_002"
    message = "File is empty"
    user_message = "The uploaded file contains no data"

class InvalidDataError(ValidationError):
    code = "VAL_003"
    message = "Invalid data values"
    user_message = "Invalid values found: {details}"

class MissingPortfoliosError(ValidationError):
    code = "VAL_004"
    message = "Portfolios missing from template - processing blocked"
    user_message = "Missing portfolios found. The following portfolios are in Bulk but not in Template: {portfolios}. Please upload a new Template file with these portfolios to continue."
    blocks_processing = True
```

### Processing Errors
```python
class ProcessingError(BidOptimizerError):
    """Base for processing errors"""

class OptimizationError(ProcessingError):
    code = "PROC_001"
    message = "Optimization failed"
    user_message = "Failed to apply {optimization} optimization"

class DataCleaningError(ProcessingError):
    code = "PROC_002"
    message = "Data cleaning failed"
    user_message = "No valid rows left after filtering"

class OutputGenerationError(ProcessingError):
    code = "PROC_003"
    message = "Cannot generate output"
    user_message = "Failed to create output files"
```

## 2. Error Codes Registry

| Code | Category | Description | User Message |
|------|----------|-------------|--------------|
| FILE_001 | File | Size exceeded | File must be smaller than 40MB |
| FILE_002 | File | Wrong format | File must be Excel or CSV |
| FILE_003 | File | Read failure | Unable to read file |
| FILE_004 | File | Missing sheet | Sheet not found |
| VAL_001 | Validation | Missing columns | Missing required columns |
| VAL_002 | Validation | Empty file | File contains no data |
| VAL_003 | Validation | Invalid data | Invalid values found |
| VAL_004 | Validation | Missing portfolios | Missing portfolios from template |
| PROC_001 | Processing | Optimization failed | Failed to apply optimization |
| PROC_002 | Processing | No data after cleaning | No valid rows after filtering |
| PROC_003 | Processing | Output failed | Failed to create files |

## 3. Error Handling Strategy

### שכבת Data
```python
def read_excel(file: BytesIO) -> pd.DataFrame:
    try:
        # Check size
        if file.size > 40_000_000:
            raise FileSizeError()
        
        # Read file
        df = pd.read_excel(file)
        
        # Check empty
        if df.empty:
            raise EmptyFileError()
            
        return df
        
    except pd.errors.ParserError:
        raise FileReadError()
```

### שכבת Business
```python
def validate_template(df: pd.DataFrame) -> ValidationResult:
    errors = []
    
    try:
        # Check columns
        missing = check_missing_columns(df)
        if missing:
            errors.append(MissingColumnsError(columns=missing))
        
        # Check data
        invalid = check_invalid_data(df)
        if invalid:
            errors.append(InvalidDataError(details=invalid))
            
    except Exception as e:
        # Log original error
        logger.error(f"Validation failed: {e}")
        # Return user-friendly error
        errors.append(ValidationError("Validation failed"))
    
    return ValidationResult(errors=errors)
```

### שכבת UI
```python
def handle_upload():
    try:
        result = orchestrator.process_upload(file)
        if result['success']:
            st.success("Files uploaded successfully")
        else:
            for error in result['errors']:
                st.error(error.user_message)
                
    except BidOptimizerError as e:
        st.error(e.user_message)
        logger.error(f"{e.code}: {e.message}")
        
    except Exception as e:
        st.error("An unexpected error occurred")
        logger.critical(f"Unexpected error: {e}")
```

## 4. הודעות למשתמש

### הודעות שגיאה (אדום)
```
❌ File exceeds 40MB limit
❌ Missing required columns: Campaign ID, Ad Group ID
❌ Sheet 'Sponsored Products Campaigns' not found
❌ No valid rows after filtering
❌ Portfolio 'ABC' not found in Bulk file
```

### הודעות אזהרה (כתום)
```
⚠️ 15 rows have Bid values above 1.25
⚠️ Some portfolios marked as 'Ignore'
⚠️ File contains special characters
```

### הודעות מידע (כחול)
```
ℹ️ Processing 10,000 rows...
ℹ️ Applying Zero Sales optimization
ℹ️ Ignored portfolios: 3
```

### הודעות הצלחה (ירוק)
```
✓ Files uploaded successfully
✓ All portfolios valid
✓ Optimization complete
✓ Files ready for download
```

### Pink Notice (ורוד - לשגיאות חישוב)
```
Please note: 7 calculation errors in Zero Sales optimization
Please note: Unable to calculate bid for 12 rows
```

## 5. Logging

### Log Levels
```python
import logging

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### What to Log
```python
# INFO - תחילה/סיום של תהליכים
logger.info(f"Starting validation for {filename}")
logger.info(f"Completed optimization in {duration}s")

# WARNING - מצבים חריגים שלא עוצרים
logger.warning(f"Found {count} rows with invalid bids")
logger.warning(f"Portfolio '{name}' marked as Ignore")

# ERROR - שגיאות שטופלו
logger.error(f"Failed to read file: {e}")
logger.error(f"Validation failed: {errors}")

# CRITICAL - שגיאות לא צפויות
logger.critical(f"Unexpected error in orchestrator: {e}")
```

## 6. Error Recovery

### Graceful Degradation
```python
def process_with_fallback(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Try optimal processing
        return optimal_process(df)
    except MemoryError:
        # Fallback to chunked processing
        return chunked_process(df)
    except Exception:
        # Return original if all fails
        logger.error("Processing failed, returning original")
        return df
```

### Transaction-like Operations
```python
def save_output_files(working, clean):
    try:
        # Save working file
        working_path = save_file(working)
        
        # Save clean file
        clean_path = save_file(clean)
        
        return {'working': working_path, 'clean': clean_path}
        
    except Exception as e:
        # Rollback - delete partial files
        if working_path:
            delete_file(working_path)
        raise OutputGenerationError() from e
```

## 7. User Experience

### Progressive Disclosure
1. **רמה 1:** הודעה פשוטה למשתמש
2. **רמה 2:** פרטים נוספים ב-expander
3. **רמה 3:** טכני ב-logs

### Error Message Template
```
[Icon] [Main Message]
[Details if needed]
[Suggested Action]

Example:
❌ Missing portfolios found
The following portfolios are in the Bulk but not in Template:
• Portfolio_ABC
• Portfolio_DEF

Please upload a new Template with these portfolios.
```

## 8. Testing Error Handling

### Unit Tests
```python
def test_file_size_error():
    large_file = create_large_file(41_000_000)
    with pytest.raises(FileSizeError) as e:
        read_excel(large_file)
    assert e.value.code == "FILE_001"
```

### Integration Tests
```python
def test_error_propagation():
    # UI calls Business
    result = orchestrator.validate(invalid_file)
    # Check error reached UI level
    assert not result['success']
    assert 'FILE_002' in result['errors'][0].code
```


### הודעות שגיאה ספציפיות לאופטימיזציות

#### Zero Sales

❌ Units column required for Zero Sales optimization
❌ Clicks column required for Zero Sales optimization
⚠️ Percentage column missing - Max BA will default to 1
ℹ️ Note: No Bidding Adjustment rows found
✓ Zero Sales optimization completed: {X} rows optimized

#### אופטימיזציות אחרות
כל אופטימיזציה מגדירה את הודעות השגיאה שלה בתוך המודול שלה.