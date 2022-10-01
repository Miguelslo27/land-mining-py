import time
import pandas as pd
import constants
from imc import get_debt, get_invoice_id, request_invoice_copy
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

def get_invoice_data(_id, year):
  print('>>>>>>>>>>>>>>>>>>>>>>>>>')
  print('Getting data from ' + str(year))
  print('<<<<<<<<<<<<<<<<<<<<<<<<<')
  invoice_data = request_invoice_copy(_id, year, get_invoice_id(_id, year))

  if len(invoice_data) == 0 and int(year) - 1 > 2000:
    invoice_data = get_invoice_data(_id, year - 1, get_invoice_id(_id, year - 1))

  return invoice_data

def process_all():
  for i, row in records_df.iterrows():
    print('========================================================================')
    print('========================================================================')
    print(get_debt(row['Código Municipal']))
    debt_status = get_debt(row['Código Municipal'])

    if debt_status['status'] == constants.ERROR:
      update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', constants.ERROR)
    else:
      print('----------------')
      print('|     ' + str(debt_status['since']) + '     |')
      print('----------------')
      
      update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', debt_status['debt'])
      update_spread_content(LANDS_SPREADSHEET_NAME, f'D{i + 2}', str(debt_status['since']))
      invoice_data = get_invoice_data(row['Código Municipal'], debt_status['since'])

    if debt_status['status'] == constants.IN_DEBT:
      invoice_data = get_invoice_data(row['Código Municipal'], debt_status['since'])

    print('INVOICE DATA', invoice_data)

    if len(invoice_data) > 0:
      update_spread_content(LANDS_SPREADSHEET_NAME, f'A{i + 2}', invoice_data[0][0])
      update_spread_content(LANDS_SPREADSHEET_NAME, f'E{i + 2}', invoice_data[0][1])
      update_spread_content(LANDS_SPREADSHEET_NAME, f'F{i + 2}', invoice_data[0][2])
      update_spread_content(LANDS_SPREADSHEET_NAME, f'G{i + 2}', invoice_data[0][3])

    print('========================================================================')
    print('========================================================================')

process_all()

# Test with one code if needed
# print(get_debt(106996))
# print(get_invoice_id(106996, 2021))
# print(request_invoice_copy(106996, 2021, get_invoice_id(106996, 2021))[0][0])
