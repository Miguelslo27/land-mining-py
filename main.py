import time
import pandas as pd
from imc import get_debt
from gspread_utils import get_spread_content

gst = time.time()

st = time.time()
print('==> Get all sheet records...')
# get all the records of the data
records = get_spread_content('Terrenos la costa')
et = time.time()
elapsed_time = et - st
print('<== Sheet records ready in', elapsed_time, 'seconds!')

st = time.time()
print('==> Convert records to data frame...')
 # convert the json to dataframe with pandas
records_df = pd.DataFrame.from_dict(records)
et = time.time()
elapsed_time = et - st
print('<== Data frame ready in', elapsed_time, 'seconds!')

# get the end time
get = time.time()

# get the execution time
global_elapsed_time = get - gst
print('|============================================|')
print('| Execution time:', global_elapsed_time, 'seconds |')
print('|============================================|')

# view the top records
print(records_df.head())
