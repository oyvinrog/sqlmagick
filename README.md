
# SQLMagick Notebook Extension

## What is SQLMagick?

SQLMagick allows you to easily query various file types within your filesystem, such as Parquet, CSV, and Excel files. It enables you to write back data or work with the files as Pandas DataFrames within Python. This extension is compatible with both Jupyter Notebook and VS Code.

## Installation

To install SQLMagick, navigate to the root folder of your project and run the following command:

```
pip install -e .
```

For centrally managed Linux distributions, follow these steps:

```
sudo apt-get update
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/oyvinrog/sqlmagick.git
```

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
