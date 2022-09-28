import time
import gspread
import pandas as pd
from pyquery import PyQuery
from oauth2client.service_account import ServiceAccountCredentials
from imc import getDebt

# defining the scope of the application
scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope_app)

# authorize the clientsheet 
client = gspread.authorize(cred)

# get the sample of the Spreadsheet
sheet = client.open('Terrenos la costa')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# print(inspect.getmembers(sheet_instance, predicate = inspect.ismethod))
# print(*inspect.getmembers(sheet_instance, predicate = inspect.ismethod), sep = "\n")

# get all the records of the data
records = sheet_instance.get_all_records()

# view the data with no format
# print(*records, sep="\n")

 # convert the json to dataframe with pandas
records_df = pd.DataFrame.from_dict(records)

# view the top records
print(records_df.head())
# print(records_df.iloc(0)['Código Municipal'])

# print(getDebt(1)) # NOT FOUND
# print(getDebt(106995)) # NO DEBT
# print(getDebt(107000)) # IN DEBT

# Create a file for the result
# with open('examples/with-debt.html', 'w') as f:
#     f.write(response.text)

# Parse the result
# obj = PyQuery(getDebt(1))
# print('Result')
# print(obj('span#span__MENSAJERETORNO').text())

# Parse examples
# NOT_FOUND
# not_found = open("examples/not-found.html", 'r').read()
# not_found_obj = PyQuery(not_found)
# print('Result')
# print(not_found_obj('span#span__MENSAJERETORNO').text())

# NO_DEBT
# with_no_debt = open("examples/with-no-debt.html", 'r').read()
# with_no_debt_obj = PyQuery(with_no_debt)
# print('Result')
# print(with_no_debt_obj('span#span__MENSAJERETORNO').text())

# DEBT
# with_debt = open("examples/with-debt.html", 'r').read()
# with_debt_obj = PyQuery(with_debt)
# print('Result')
# print(float(with_debt_obj('span#span__MONTOFINAL_0001').text().replace('.', '').replace(',','.'), 2))