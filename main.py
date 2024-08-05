import sys
import time
import pandas as pd
import constants
import traceback
from datetime import datetime

from imc import get_debt, get_invoice_id, request_invoice_copy
from gspread_utils import get_spread_content, update_spread_content

LANDS_SPREADSHEET_NAME = 'Terrenos la costa'
TRACKING_PATH = f'last_land_id.txt'
ROW_INDEX_ID_PATH = f'row_index_id.txt'
ACTUAL_YEAR = datetime.now().year

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

  print(len(invoice_data))

  if len(invoice_data) == 0 and int(year) - 1 >= 1998:
    invoice_data = get_invoice_data(_id, year - 1)

  return invoice_data

def process_all():
  invoice_data = []
  
  # for i, row in records_df.iterrows():
  row_index = int(open(ROW_INDEX_ID_PATH, 'r').read());
  next_id = int(open(TRACKING_PATH, 'r').read())

  while True:
    # Read the last land ID saved and start from the next
    # last_id = int(open(TRACKING_PATH, 'r').read())
    # print(int(row['Código Municipal']), last_id)

    # if int(row['Código Municipal']) <= last_id:
    #   continue

    debt_status = get_debt(next_id)
    print(debt_status)

    try:
      update_spread_content(LANDS_SPREADSHEET_NAME, f'B{row_index}', next_id)

      if debt_status['status'] == constants.ERROR:
        update_spread_content(LANDS_SPREADSHEET_NAME, f'C{row_index}', constants.ERROR)
      elif debt_status['status'] == constants.NOT_FOUND:
        update_spread_content(LANDS_SPREADSHEET_NAME, f'C{row_index}', constants.NOT_FOUND)
      else:
        print('      DEBT      ')
        print('----------------')
        print('|     ' + str(debt_status['since']) + '     |')
        print('----------------')
        
        update_spread_content(LANDS_SPREADSHEET_NAME, f'C{row_index}', debt_status['debt'])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'D{row_index}', str(debt_status['since']))
        invoice_data = get_invoice_data(next_id, ACTUAL_YEAR)

      if debt_status['status'] == constants.IN_DEBT:
        invoice_data = get_invoice_data(next_id, ACTUAL_YEAR)

      print('INVOICE DATA', invoice_data)

      if len(invoice_data) > 0:
        update_spread_content(LANDS_SPREADSHEET_NAME, f'A{row_index}', invoice_data[0][0])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'E{row_index}', invoice_data[0][1])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'F{row_index}', invoice_data[0][2])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'G{row_index}', invoice_data[0][3])
    except:
      print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
      print('An exception occurred: ', traceback.format_exc())
      print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
      print(int(next_id), next_id + 1)
      time.sleep(10)

    print('========================================================================')
    print('========================================================================')
    row_index += 1
    open(ROW_INDEX_ID_PATH, 'w').write(str(row_index))

    # Save last land id checked
    next_id += 1
    open(TRACKING_PATH, 'w').write(str(next_id))

process_all()

# Test with one code if needed
# print('========================================================================')
# print('========================================================================')
# print('DEBT', get_debt(107000))
# print('INVOICE ID', get_invoice_id(107000, 2022))
# print('INVOICE COPY', get_invoice_data(107000, 2022))
# print('========================================================================')
# print('========================================================================')
# print(request_invoice_copy(106999, 2021, get_invoice_id(106999, 2021))[0][0])
