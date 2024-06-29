## Installation

Navigate to the root folder and run: "pip install -e ."


## Example usage

-----cell 1-----

%load_ext sqlmagick

-----cell 2-----

%%dump_xls 

C:\temp\errorparser


------cell 3------

%%sql

select * from output_sheet1

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

