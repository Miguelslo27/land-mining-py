import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_spreadsheet(spname):
  # defining the scope of the application
  scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

  st = time.time()
  print('==> Get service account credentials...')
  #credentials to the account
  cred = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope_app)
  et = time.time()
  elapsed_time = et - st
  print('<== Service account credentials ready in', elapsed_time, 'seconds!')

  st = time.time()
  print('==> Get Google Spreadsheet client...')
  # authorize the clientsheet 
  client = gspread.authorize(cred)
  et = time.time()
  elapsed_time = et - st
  print('<== Google Spreadsheet client ready in', elapsed_time, 'seconds!')

  st = time.time()
  print('==> Get spreadsheet "', spname, '"...')
  # get the sample of the Spreadsheet
  sheet = client.open(spname)
  et = time.time()
  elapsed_time = et - st
  print('<== Spreadsheet "', spname, '" ready in', elapsed_time, 'seconds!')

  st = time.time()
  print('==> Get first worksheet...')
  # get the first sheet of the Spreadsheet
  sheet_instance = sheet.get_worksheet(0)
  et = time.time()
  elapsed_time = et - st
  print('<== Worksheet ready in', elapsed_time, 'seconds!')

  return sheet_instance
