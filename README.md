## Installation

Navigate to the root folder and run: "pip install -e ."

On centrally managed Linux distributions:

```
sudo apt-get update
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/oyvinrog/sqlmagick.git
```


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

