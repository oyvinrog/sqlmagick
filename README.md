
# SQLMagick Notebook Extension

## What is SQLMagick?

SQLMagick allows you to easily query various file types within your filesystem, such as Parquet, CSV, and Excel files. It enables you to write back data or work with the files as Pandas DataFrames within Python. This extension is compatible with both Jupyter Notebook and VS Code.

## Installation

To install SQLMagick:

```bash
pip install git+https://github.com/oyvinrog/sqlmagick.git
```

For centrally managed Linux distributions, set up a virtual environment:

```bash
sudo apt-get update
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/oyvinrog/sqlmagick.git
```

## Setting up "Query with SQLMagick" for Windows 

To set up the ability to right click on a file and query it with SQLMagick, follow these steps:

1. Run cmd as administrator.
2. Run setup_registry.bat 

If you regret, run disable_registry.bat.



## Example Usage

### Cell 1: Load SQLMagick Extension

```
%load_ext sqlmagick
```

### Cell 2: Dump Files

```
%%dump_files
C:\temp\errorparser\error*.csv
```

### Cell 3: Execute SQL Query

```sql
%%sql

SELECT * FROM output_sheet1
```

### Cell 4: Output Results to a Parquet File

In this example, we output the results to `strange_errors.parquet`:

```sql
%%sql strange_errors.parquet

SELECT * FROM output_sheet1
WHERE error_message LIKE '%infinite recursion%'
```

### Cell 5: Output Results to a Delta Table

In this example, we output the results to `strange_errors.delta`:

```sql
%%sql strange_errors.delta

SELECT * FROM output_sheet1
WHERE error_message LIKE '%infinite recursion%'
```


## Creating Temporary Tables

To create a temporary table in the database, use the following syntax:

```sql
%%createtemp temp_table

SELECT * FROM customers WHERE customer_id=4
```

## Tips

To increase the number of columns displayed in the notebook, use the following Pandas option:

```
pd.set_option('display.max_columns', 500)
```

## Development

If you do a change, reinstall using 

`pip install --upgrade .` from the root directory