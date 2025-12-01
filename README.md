Data UtilsA collection of Python utilities for data processing and comparison.Project Structuredata_utils/
├── utils/                 # Source code package
│   ├── __init__.py        # Makes 'utils' a Python package
│   └── csv_compare.py     # The CSV comparison tool
├── requirements.txt       # List of dependencies
├── setup.py               # Installation script
└── README.md              # Documentation
SetupClone or download this repository.Create a virtual environment (recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:pip install -r requirements.txt
Install the package in editable mode (allows you to run tools from anywhere):pip install -e .
UsageCSV ComparatorCompares two CSV files based on a specific primary key column. It identifies missing rows and column mismatches.Command Line Usage:You can run the script directly as a module:python -m utils.csv_compare path/to/file1.csv path/to/file2.csv PrimaryKeyColumn
Options:--limit or -n: Limit the number of differences displayed (default: 10).Example:python -m utils.csv_compare data_2023.csv data_2024.csv UserID -n 20
Adding New ToolsTo add a new tool (e.g., a JSON validator):Create a new file in the utils/ folder (e.g., utils/json_validate.py).Add a main() function and an if __name__ == "__main__": block.Run it using python -m utils.json_validate ....