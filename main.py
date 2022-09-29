import time
import pandas as pd
import constants
from imc import get_debt
from gspread_utils import get_spread_content, update_spread_content

LANDS_SPREADSHEET_NAME = 'Terrenos la costa'

gst = time.time()

st = time.time()
print('==> Get all sheet records...')
# get all the records of the data
records = get_spread_content(LANDS_SPREADSHEET_NAME)
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

for i, row in records_df.iterrows():
  print(get_debt(row['Código Municipal']))
  debt_status = get_debt(row['Código Municipal'])

  if debt_status['status'] == constants.ERROR:
    update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', constants.ERROR)
  else:
    update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', debt_status['debt'])

  if debt_status['status'] == constants.IN_DEBT:
    update_spread_content(LANDS_SPREADSHEET_NAME, f'D{i + 2}', debt_status['since'])

  print('=====================')

# Test with one code if needed
# print(get_debt(107010))
