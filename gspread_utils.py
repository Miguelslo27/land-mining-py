import json
import os.path
import time
import re
import unicodedata
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

def get_spreadsheet(spname):
  st = time.time()
  print('==> Get spreadsheet "', spname, '"...')
  # get the sample of the Spreadsheet
  sheet = client.open(spname)
  print('soooooo')
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

def get_spread_content(spname):
   # sanitize spname
  path_to_cache = f'cache/{sanitize_text(spname)}.json'

  # check file for spname
  if os.path.exists(path_to_cache) == True:
    st = time.time()
    print('==> Get spread content from cache...')
    #credentials to the account
    # cred = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope_app)
    cache_content = open(path_to_cache, 'r').read()
    et = time.time()
    elapsed_time = et - st
    print('<== Spread content from cache ready in', elapsed_time, 'seconds!')

    return json.loads(cache_content)
  else:
    spreadsheet_content = get_spreadsheet(spname).get_all_records()
    # Create a file for the result
    st = time.time()
    print('==> Save content to cache...')

    with open(path_to_cache, 'w') as f:
      f.write(json.dumps(spreadsheet_content))

    et = time.time()
    elapsed_time = et - st
    print('<== Content saved in cache ready in', elapsed_time, 'seconds!')

    return spreadsheet_content

def update_spread_content(spname, cell, value):
  get_spreadsheet(spname).update(cell, value)

def strip_accents(text):
  """
  Strip accents from input String

  :param text: The input string
  :type text: String.

  :returns: The processed String
  :rtype: String.
  """
  try:
      text = unicode(text, 'utf-8')
  except (TypeError, NameError): # unicode is a default on python 3
      pass
  text = unicodedata.normalize('NFD', text)
  text = text.encode('ascii', 'ignore')
  text = text.decode("utf-8")
  return str(text)

def sanitize_text(text):
  """
  Convert input text to id.

  :param text: The input string
  :type text: String.

  :returns: The processed String
  :rtype: String.
  """
  text = strip_accents(text.lower())
  text = re.sub('[ ]+', '_', text)
  text = re.sub('[^0-9a-zA-Z_-]', '', text)
  return text
