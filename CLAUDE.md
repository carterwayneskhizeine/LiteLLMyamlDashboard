# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based AI Models Dashboard application that processes and displays AI model configuration data. The system transforms raw YAML configuration files into a clean, filterable table view.

## Architecture

### Core Components

1. **app.py** - Streamlit Web Application
   - Main dashboard interface
   - Reads processed YAML data and displays it in a filterable table
   - Features filtering by input/output costs, reasoning/vision support, and free models
   - Includes import functionality for uploading new YAML configurations
   - Includes CCR model sync button for syncing to Claude Code Router
   - Displays models with columns: Model Name, Input Cost ($/1M), Output Cost ($/1M), Max Context, Max Output, Reasoning, Vision

2. **process_yaml.py** - YAML Processing Script
   - Transforms raw model configurations to standardized format
   - Converts per-token costs to per-1M tokens costs
   - Formats token limits (e.g., 128000 → 128K)
   - Can be used via command line or imported as a module
   - Returns success/failure status with detailed messages

3. **sync_ccr_models.py** - CCR Model Sync Script
   - Extracts model names from litellmconfig.yaml's model_list
   - Updates config.json's lite provider models array
   - Includes UTF-8 encoding handling for Windows compatibility
   - Can be used via command line or triggered from app.py
   - Returns success/failure status with detailed messages

4. **processed_models.yaml** - Data File (Generated)
   - Standardized model configuration data
   - Used by app.py for display
   - Format: `{'model_list': [{'model_name': '...', 'model_info': {...}}]}`

5. **litellmconfig.yaml** - Source Data File (Original)
   - Raw model configuration with per-token pricing
   - Processed by process_yaml.py
   - Source for model names in sync_ccr_models.py

6. **config.json** - Claude Code Router Configuration
   - CCR configuration file with Providers array
   - Updated by sync_ccr_models.py
   - Contains lite provider with models array

### Data Flow

**Dashboard Display Flow:**
```
litellmconfig.yaml (raw)
    ↓
process_yaml.py (transform)
    ↓
processed_models.yaml (standardized)
    ↓
app.py (display & filter)
```

**CCR Sync Flow:**
```
litellmconfig.yaml (model_list)
    ↓
sync_ccr_models.py (extract & update)
    ↓
config.json (lite provider models)
```

## Development Commands

### Running the Application

```bash
# Start the Streamlit dashboard
streamlit run app.py
```

### Processing YAML Files

```bash
# Process with default files
python process_yaml.py

# Process with custom input/output
python process_yaml.py input.yaml output.yaml

# Process litellmconfig.yaml to processed_models.yaml (default)
python process_yaml.py litellmconfig.yaml processed_models.yaml
```

### Syncing CCR Models

```bash
# Sync with default paths
python sync_ccr_models.py

# Sync with custom paths
python sync_ccr_models.py <yaml_file> <json_file>

# Example with specific paths
python sync_ccr_models.py C:\Users\user\litellmconfig.yaml C:\Users\user\.claude-code-router\config.json
```

### Dependencies

Required packages:
- streamlit
- pyyaml
- pandas

## Key Features

### Filtering (app.py)
- **Price Range**: Filter by minimum/maximum input/output costs
- **Feature Support**: Filter models supporting reasoning or vision
- **Free Models**: Toggle to show only free models (0 cost)
- **Search**: Text search in model names

### Import Functionality (app.py)
- Click "导入配置" button in sidebar
- Upload YAML file (.yaml or .yml format)
- System automatically processes file and updates dashboard
- Temporary files cleaned up after processing

### CCR Model Sync (app.py)
- Click "🔄 Sync CCR Models" button at bottom of sidebar
- Automatically extracts all model names from litellmconfig.yaml
- Updates config.json's lite provider models array
- Shows success/failure message with expandable details
- Handles subprocess execution with UTF-8 encoding

### UI Structure
- Left sidebar: All filters, import buttons, and CCR sync button
- Main area: Model data table with row numbers (# column)
- Clean, minimal interface without headers or metric cards
- CCR sync button located at bottom of sidebar with separator

## Important Implementation Details

### Caching (app.py)
- `load_data()` function uses `@st.cache_data(show_spinner=False)` decorator
- Call `st.cache_data.clear()` to refresh cached data
- Session state variables track import workflow:
  - `st.session_state.show_uploader`
  - `st.session_state.uploaded_file_path`
  - `st.session_state.data_updated`

### Error Handling
- process_yaml.py includes comprehensive exception handling
- Returns tuple: `(success: bool, message: str)`
- Handles FileNotFoundError, YAML parsing errors, and generic exceptions

### Data Transformations (process_yaml.py)
- Cost conversion: `cost_per_token * 1,000,000` → rounded to 2 decimal places
- Token formatting: `128000` → `"128K"`
- Handles division by zero for token limits
- Preserves boolean flags (supports_reasoning, supports_vision) only when True

### CCR Model Sync Logic (sync_ccr_models.py)
- Reads litellmconfig.yaml using yaml.safe_load
- Extracts model_name from each item in model_list array
- Reads config.json and finds provider with name="lite"
- Replaces entire models array with extracted model names
- Writes back to config.json with proper JSON formatting (indent=2)
- Uses UTF-8 encoding throughout to avoid Windows GBK issues

### Windows Encoding Handling
- sync_ccr_models.py sets stdout/stderr to UTF-8 on Windows
- app.py subprocess call uses encoding='utf-8' parameter
- Avoids UnicodeEncodeError with special characters
- Uses text markers [SUCCESS]/[ERROR] instead of Unicode symbols in script output

### File Structure
```
D:\Code\LiteLLMyamlDashboard\
├── app.py                    # Streamlit application
├── process_yaml.py           # YAML processing script
├── sync_ccr_models.py        # CCR model sync script
├── processed_models.yaml     # Generated data file
├── litellmconfig.yaml        # Source data file (not in repo)
├── config.json               # CCR configuration file
├── README.md                 # User documentation
├── CLAUDE.md                 # Developer documentation
└── temp_uploads/             # Temporary upload directory (created at runtime)
```

## Common Development Tasks

### Adding New Filter Options
1. Add UI control in app.py sidebar section (after existing filters)
2. Add filtering logic before "应用过滤器" section
3. Update DataFrame operations accordingly

### Modifying Table Columns
1. Edit `column_names` dictionary in app.py
2. Adjust `cols` array in `load_data()` function to set column order
3. Add formatting logic if needed

### Changing Data Processing Logic
1. Modify `process_model_list()` function in process_yaml.py
2. Update data transformation rules (cost conversion, token formatting, etc.)
3. Maintain backward compatibility with existing YAML structure

### Testing Import Functionality
1. Use the sidebar "导入配置" button
2. Upload test YAML file with `model_list` structure
3. Click "开始处理" to process
4. Click "刷新数据" to reload if needed

### Testing CCR Sync Functionality
1. Use the sidebar "🔄 Sync CCR Models" button
2. Check success/failure message in sidebar
3. Expand "查看详情" to see full output
4. Verify config.json was updated correctly
5. Test with command line: `python sync_ccr_models.py`

### Adding CCR Sync to Other Workflows
1. Import sync_ccr_models module: `from sync_ccr_models import sync_models`
2. Call function: `success, message = sync_models(yaml_path, json_path)`
3. Handle return tuple for success/failure
4. Display message appropriately in UI

## Usage Notes

- The app automatically clears cache when data is updated via import
- Temporary upload files are stored in `temp_uploads/` directory
- All filters work in combination (AND logic)
- Empty results show an empty table with no error message
- Index numbers (# column) start from 1 and reflect filtered results
- CCR sync button uses subprocess with 30-second timeout
- CCR sync updates config.json in-place (no backup created)
- CCR sync reads from litellmconfig.yaml and writes to config.json
- Script outputs are displayed in expandable panels in sidebar
