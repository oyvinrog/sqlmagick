"""
Magic functions for working with SQL, Excel, and Parquet files in Jupyter notebooks.

How to load from notebook: %load_ext sqlmagick

%%sql - Execute SQL queries and return the result as a Pandas DataFrame.
    
                Parameters: optional file path for saving the result as a Parquet file
                If you suffix as .delta, it will save as a delta table

%%dump_files - Load Excel, CSV, and Parquet files from a folder for querying. Parameters: folder path
               TIP: if you just want to use the current directory, just use %%dump_files with a dot (.)

               Wildcards are supported, e.g., %%dump_files *.csv will load all CSV files in the current directory.

%%dump_df - Load a DataFrame into the database. Parameters: DataFrame

%%load_df - Load a table into a dataframe in the notebook. Parameters: table name

            use your_df = _ to assign the results to a dataframe locally

%%createtemp - Create a temporary table in the database. Parameters: table name, SQL
"""

import os
import pandas as pd
import traceback
import sqlite3
from IPython.core.magic import (register_line_magic, register_cell_magic, register_line_cell_magic, needs_local_scope)
from IPython import get_ipython
from IPython.display import display, HTML
import re
import glob
from deltalake.writer import write_deltalake
import duckdb

@register_cell_magic
@needs_local_scope
def sql(line, cell, local_ns=None):
    # Split the line to get any potential file path for dumping the result
    args = line.split()
    output_file = None
    if len(args) > 0:
        # Assuming the first argument is the file path if provided
        output_file = args[0]

    try:
        # Reopen the connection
        with sqlite3.connect('sqlmagick.db') as conn:
            cursor = conn.cursor()
            query = cell.strip()  # SQL query from the cell
            query_type = query.split()[0].upper()  # Determine the type of SQL statement
            
            if query_type in ['UPDATE', 'DELETE', 'INSERT']:
                # Handle DML statements
                cursor.execute(query)
                conn.commit()
                print(f"{query_type} executed successfully.")
            else:
                # Handle other SQL queries and return result as a dataframe
                result = pd.read_sql_query(query, conn)
                if output_file:
                    if output_file.endswith('.parquet'):
                        # Save result to a Parquet file
                        result.to_parquet(output_file)
                        print(f"Query result saved to {output_file}")
                    elif output_file.endswith('.delta'):
                        # Save result to a Delta table
                        write_deltalake(output_file, result)
                        print(f"Query result saved to Delta table at {output_file}")
                    else:
                        print(f"Unsupported file format: {output_file}")
                else:
                    return result
    except Exception as e:
        print(f"An error occurred in %%sql: {str(e)}")
        traceback.print_exc()

@register_cell_magic
@needs_local_scope
def dump_files(line, cell, local_ns=None):
    pattern = cell.strip()  # The directory to scan for files, passed in the cell
    
    db_path = 'sqlmagick.db'
    
    # Connect to the SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Use glob to match patterns and collect files
        files_to_process = glob.glob(pattern, recursive=True)
        files_to_process = [file for file in files_to_process if file.endswith(('.xlsx', '.xls', '.csv', '.parquet'))]
        
        for file_path in files_to_process:
            file = os.path.basename(file_path)
            if file.endswith('.xlsx') or file.endswith('.xls'):
                try:
                    # Load each sheet into the database
                    xls = pd.ExcelFile(file_path)
                    for sheet_name in xls.sheet_names:
                        print(f"Reading \"{sheet_name}\" from {file}")
                        try:
                            df = pd.read_excel(file_path, sheet_name=sheet_name)
                            # Sanitize column names
                            df.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]
                            # Create a normalized table name based on the file and sheet names
                            table_name = f"{os.path.splitext(file)[0].replace(' ', '_')}_{sheet_name.replace(' ', '_')}"
                            # Remove <>
                            table_name = re.sub(r'<|>', '', table_name)
                            print(f"Loading {sheet_name} from {file} into {table_name}")
                            if len(df.columns) == 0:
                                print(f"Warning: {file} has no columns. Skipping.")
                                continue 

                            df.to_sql(table_name, conn, if_exists='replace', index=False)
                            
                            display(HTML(f"<span style='background-color: green;'>Loaded {sheet_name} from {file} into {table_name}</span>"))
                            print("Closing connection")
                            conn.close()

                        except Exception as e:
                            print(f"Failed to load sheet {sheet_name} from {file}: {str(e)}")
                            display(HTML(f"<span style='background-color: yellow;'>Warning: Failed to load sheet {sheet_name} from {file}</span>"))
                            # Show stack trace
                            traceback.print_exc()
                
                except Exception as e:
                    print(f"Failed to load {file_path}: {str(e)}")
                    # Show stack trace
                    traceback.print_exc()

            elif file.endswith(".csv"):
                try:
                    df = pd.read_csv(file_path)
                    # Sanitize column names
                    df.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]
                    # Create a normalized table name based on the file name
                    table_name = f"{os.path.splitext(file)[0].replace(' ', '_')}"

                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    print(f"Loaded {file} into {table_name}")
            
                except Exception as e:
                    print(f"Failed to load {file_path}: {str(e)}")
                    # Show stack trace
                    traceback.print_exc()

            elif file.endswith(".parquet"):
                try:
                    df = pd.read_parquet(file_path)
                    # Sanitize column names
                    df.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]
                    # Create a normalized table name based on the file name
                    table_name = f"{os.path.splitext(file)[0].replace(' ', '_')}"
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    print(f"Loaded {file} into {table_name}")
            
                except Exception as e:
                    print(f"Failed to load {file_path}: {str(e)}")
                    # Show stack trace
                    traceback.print_exc()

        # Additional step to handle .delta folders
        if os.path.isdir(pattern) and pattern.endswith('.delta'):
            delta_folders = [pattern]
        else:
            delta_folders = glob.glob(os.path.join(pattern, '*.delta'), recursive=True)
        
        for delta_folder in delta_folders:
            try:
                # Use duckdb to read the Delta table
                con = duckdb.connect()
                stmt = f"""
                SELECT *
                FROM delta_scan('{delta_folder}')
                """
                results = con.execute(stmt).fetchdf()
                # Sanitize column names
                results.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in results.columns]
                # Create a normalized table name based on the folder name
                table_name = os.path.basename(delta_folder).replace('.delta', '').replace(' ', '_')
                results.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Loaded Delta table from {delta_folder} into {table_name}")
            except Exception as e:
                print(f"Failed to load Delta table from {delta_folder}: {str(e)}")
                # Show stack trace
                traceback.print_exc()

    except Exception as e:
        print(f"An error occurred in %%dump_files: {str(e)}")
        traceback.print_exc()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

@register_cell_magic
@needs_local_scope
def dump_df(line, cell, local_ns=None):
    df = local_ns[cell.strip()]  # The DataFrame to load into the database
    table_name = cell.strip()
    db_path = 'sqlmagick.db'

    # Connect to the SQLite database
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Loaded DataFrame into {table_name}")

@register_cell_magic
@needs_local_scope
def load_df(line, cell, local_ns=None):
    table_name = cell.strip()  # The table name to load from the database
    db_path = 'sqlmagick.db'

    # Connect to the SQLite database
    with sqlite3.connect(db_path) as conn:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        local_ns[table_name] = df  # Optionally load it into the local namespace if needed
        return df

@register_cell_magic
@needs_local_scope
def createtemp(line, cell, local_ns=None):
    table_name = line.strip()  # Get the table name from the line
    sql_query = cell.strip()  # Get the SQL query from the cell
    db_path = 'sqlmagick.db'

    # Connect to the SQLite database
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(sql_query, conn)  # Execute the query and store the result in a DataFrame
        df.to_sql(table_name, conn, if_exists='replace', index=False)  # Create a new table from the DataFrame
        print(f"Temporary table {table_name} created successfully with data from query")

def load_ipython_extension(ipython):
    # Register the magic functions with IPython
    ipython.register_magic_function(sql, 'cell')
    ipython.register_magic_function(dump_files, 'cell')
    ipython.register_magic_function(dump_df, 'cell')
    ipython.register_magic_function(load_df, 'cell')
    ipython.register_magic_function(createtemp, 'cell')

def unload_ipython_extension(ipython):
    pass
