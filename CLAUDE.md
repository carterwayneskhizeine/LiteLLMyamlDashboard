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
   - Displays models with columns: Model Name, Input Cost ($/1M), Output Cost ($/1M), Max Context, Max Output, Reasoning, Vision

2. **process_yaml.py** - YAML Processing Script
   - Transforms raw model configurations to standardized format
   - Converts per-token costs to per-1M tokens costs
   - Formats token limits (e.g., 128000 → 128K)
   - Can be used via command line or imported as a module
   - Returns success/failure status with detailed messages

3. **processed_models.yaml** - Data File (Generated)
   - Standardized model configuration data
   - Used by app.py for display
   - Format: `{'model_list': [{'model_name': '...', 'model_info': {...}}]}`

4. **litellmconfig.yaml** - Source Data File (Original)
   - Raw model configuration with per-token pricing
   - Processed by process_yaml.py

### Data Flow

```
litellmconfig.yaml (raw)
    ↓
process_yaml.py (transform)
    ↓
processed_models.yaml (standardized)
    ↓
app.py (display & filter)
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

### UI Structure
- Left sidebar: All filters and import buttons
- Main area: Model data table with row numbers (# column)
- Clean, minimal interface without headers or metric cards

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

### File Structure
```
D:\Code\yamltomarkdown\
├── app.py                    # Streamlit application
├── process_yaml.py           # YAML processing script
├── processed_models.yaml     # Generated data file
├── litellmconfig.yaml        # Source data file (not in repo)
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

## Usage Notes

- The app automatically clears cache when data is updated via import
- Temporary upload files are stored in `temp_uploads/` directory
- All filters work in combination (AND logic)
- Empty results show an empty table with no error message
- Index numbers (# column) start from 1 and reflect filtered results
