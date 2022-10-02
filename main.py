import sys
import time
import pandas as pd
import constants
from imc import get_debt, get_invoice_id, request_invoice_copy
from gspread_utils import get_spread_content, update_spread_content

LANDS_SPREADSHEET_NAME = 'Terrenos la costa'
TRACKING_PATH = f'last_land_id.txt'

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

  if len(invoice_data) == 0 and int(year) - 1 >= 1998:
    invoice_data = get_invoice_data(_id, year - 1)

  return invoice_data

def process_all():
  for i, row in records_df.iterrows():
    # Read the last land ID saved and start from the next
    last_id = int(open(TRACKING_PATH, 'r').read())
    print(int(row['Código Municipal']), last_id)

    if int(row['Código Municipal']) <= last_id:
      continue
    
    debt_status = get_debt(row['Código Municipal'])
    print(debt_status)

    try:
      if debt_status['status'] == constants.ERROR:
        update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', constants.ERROR)
      elif debt_status['status'] == constants.NOT_FOUND:
        update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', constants.NOT_FOUND)
      else:
        print('      DEBT      ')
        print('----------------')
        print('|     ' + str(debt_status['since']) + '     |')
        print('----------------')
        
        update_spread_content(LANDS_SPREADSHEET_NAME, f'C{i + 2}', debt_status['debt'])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'D{i + 2}', str(debt_status['since']))
        invoice_data = get_invoice_data(row['Código Municipal'], 2022)

      if debt_status['status'] == constants.IN_DEBT:
        invoice_data = get_invoice_data(row['Código Municipal'], 2022)

      print('INVOICE DATA', invoice_data)

      if len(invoice_data) > 0:
        update_spread_content(LANDS_SPREADSHEET_NAME, f'A{i + 2}', invoice_data[0][0])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'E{i + 2}', invoice_data[0][1])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'F{i + 2}', invoice_data[0][2])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'G{i + 2}', invoice_data[0][3])
        update_spread_content(LANDS_SPREADSHEET_NAME, f'H{i + 2}', invoice_data[1])
    except:
      print('∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆')
      print(sys.exc_info()[0])
      print('∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆')
      last_id = int(open(TRACKING_PATH, 'r').read())
      print(int(row['Código Municipal']), last_id - 1)
      time.sleep(30)

    print('========================================================================')
    print('========================================================================')

    # Save last land id checked
    open(TRACKING_PATH, 'w').write(str(row['Código Municipal']))

process_all()

# Test with one code if needed
# print('========================================================================')
# print('========================================================================')
# print('DEBT', get_debt(106083))
# print('INVOICE ID', get_invoice_id(106083, 2022))
# print('INVOICE COPY', get_invoice_data(106083, 2022))
# print('========================================================================')
# print('========================================================================')
# print(request_invoice_copy(106999, 2021, get_invoice_id(106999, 2021))[0][0])
