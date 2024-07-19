## Installation

Navigate to the root folder and run: "pip install -e ."

on centrally managed Linux distributions, I have no clue how to handle this.
Just copy sqlmagick.py into the same folder as your .ipynb file


## Example usage

-----cell 1-----

%load_ext sqlmagick

-----cell 2-----

%%dump_files 

C:\temp\errorparser\error*.csv


------cell 3------

%%sql

select * from output_sheet1


----Cell 4--------
In this example, we output the results to strange_errors.parquet

%%sql strange_errors.parquet

select * from output_sheet1
where error_message like '%infinite recursion%'



### Creating temp tables

Create temp_table in the database:

```
%%createtemp temp_table
SELECT * FROM customers WHERE customer_id=4
```

## Tips

Use 

pd.set_option('display.max_columns', 500)

to increase the number of columns displayed in the notebook

