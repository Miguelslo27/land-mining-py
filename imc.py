import re
from urllib import request
import requests
import constants
from pyquery import PyQuery

# curl 'https://tributos.imcanelones.gub.uy:8443/cows/servlet/hconsultadeudawebcan' \
#   -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
#   -H 'Accept-Language: es-ES,es;q=0.9' \
#   -H 'Cache-Control: max-age=0' \
#   -H 'Connection: keep-alive' \
#   -H 'Content-Type: application/x-www-form-urlencoded' \
#   -H 'Cookie: GX_SESSION_ID=yc3pgQrDDoqd0skF0%2B8F%2FrvpZZ4cKCYBwIQom7rRGrM%3D; JSESSIONID=5D3F3E6F9D29ED953451CECBE1474BF5; _fbp=fb.2.1663724475802.786148759; _ga=GA1.3.1227441019.1663724478' \
#   -H 'Origin: https://tributos.imcanelones.gub.uy:8443' \
#   -H 'Referer: https://tributos.imcanelones.gub.uy:8443/cows/servlet/hconsultadeudawebcan' \
#   -H 'Sec-Fetch-Dest: document' \
#   -H 'Sec-Fetch-Mode: navigate' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'Sec-Fetch-User: ?1' \
#   -H 'Upgrade-Insecure-Requests: 1' \
#   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
#   -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   --data-raw '_EventName=E%27CONSULTA+DE+DEUDA%27.&_EventGridId=20&_EventRowId=1&_IDPADRON=1&BUTTON1=Buscar&_SANIO_0001=&_VTO_0001=&_CODIGOCONCEPTO_0001=&_CONCEPTO_0001=SUBTOTAL&_CUOTA_0001=&_IMPORTE_0001=0.00&_LINEA_0001=0&_MENSAJERETORNO=Padr%C3%B3n+inexistente&_MONTOFINAL_0001=0%2C00&_AUXILIARCOBRO=0&_VALPAR=&_NUMEROPREFACTURA=0&_NROPARAMETRO=0&_TIPOBUSQUEDA=0&_CODIGORETORNO=001&_PADRON=&nRC_Grilladeuda=1&nRC_Grilladetalle=0&nRC_Grillapago=0&nRC_Grillatotal=1&sCallerURL=' \
#   --compressed

def get_debt(_id):
  data = {
    '_EventName': 'E\'CONSULTA DE DEUDA\'.',
    '_EventGridId': '20',
    '_EventRowId': '1',
    '_IDPADRON': _id,
    'BUTTON1': 'Buscar',
    '_SANIO_0001': '',
    '_VTO_0001': '',
    '_CODIGOCONCEPTO_0001': '',
    '_CONCEPTO_0001': 'SUBTOTAL',
    '_CUOTA_0001': '',
    '_IMPORTE_0001': '0.00',
    '_LINEA_0001': '0',
    '_MENSAJERETORNO': 'Padrón inexistente',
    '_MONTOFINAL_0001': '0,00',
    '_AUXILIARCOBRO': '0',
    '_VALPAR': '',
    '_NUMEROPREFACTURA': '0',
    '_NROPARAMETRO': '0',
    '_TIPOBUSQUEDA': '0',
    '_CODIGORETORNO': '001',
    '_PADRON': '',
    'nRC_Grilladeuda': '1',
    'nRC_Grilladetalle': '0',
    'nRC_Grillapago': '0',
    'nRC_Grillatotal': '1',
    'sCallerURL': '',
  }

  response = request_imc('post', 'hconsultadeudawebcan', data)

  # To test when some error occur
  # with open('examples/error.html', 'w') as f:
  #   f.write(response.text)

  obj = PyQuery(response.text)
  message = obj('span#span__MENSAJERETORNO').text()
  debt = obj('span#span__MONTOFINAL_0001').text()
  debt = float(debt.replace('.', '').replace(',','.'))
  debt_since = obj('span#span__SANIO_0001').text()

  land_data = dict();

  if message == constants.NOT_FOUND_MSG:
    land_data['status'] = constants.NOT_FOUND
    land_data['since'] = 0
    land_data['debt'] = 0
  elif message == constants.NO_DEBT_MSG:
    land_data['status'] = constants.NO_DEBT
    land_data['since'] = 0
    land_data['debt'] = 0
  elif debt > 0:
    land_data['status'] = constants.IN_DEBT
    land_data['since'] = debt_since
    land_data['debt'] = debt
  else:
    land_data['status'] = constants.ERROR
    land_data['since'] = 0
    land_data['debt'] = 0

  return land_data

def get_invoice_id(_id, year):
  data = {
    '_EventName': 'E\'BUSCARCOBROS\'.',
    '_EventGridId': '24',
    '_EventRowId': '1',
    '_IDPADRON': _id,
    '_BUSCAR': '',
    '_ANIO': year,
    'BUTTON1': 'Buscar',
    '_MENSAJERETORNO': '',
    'nRC_Grillacobros': '0',
    'sCallerURL': 'https://tributos.imcanelones.gub.uy:8443/cows/servlet/himprimirduplicadoperiodo',
    '_TODAY': '2022-09-28',
  }

  response = request_imc('post', 'himprimirduplicadoperiodo', data)

  obj = PyQuery(response.text)
  invoice_id = obj('span#span__COBNRO_0001').text()

  # To test when some error occur
  # file_path = f'examples/invoices/copy_{_id}_{year}.html'
  # with open(file_path, 'w') as f:
  #   f.write(response.text)

  return invoice_id

def request_invoice_copy(_id, year, invoice_id):
  data = {
    '_EventName': 'E\'VERCOBRO\'.0001',
    '_EventGridId': '',
    '_EventRowId': '',
    '_IDPADRON': _id,
    '_BUSCAR': 'S',
    '_ANIO': year,
    '_MENSAJERETORNO': '',
    'GXimg_IMPRIMIR_0001': 'bigfolder.gif',
    '_COBNRO_0001': invoice_id,
    '_FECHA_0001': '05/02/2021',
    '_IMPORTE_0001': '2650,00',
    'GXimg_IMPRIMIR_0002': 'bigfolder.gif',
    '_COBNRO_0002': '508924171',
    '_FECHA_0002': '09/04/2021',
    '_IMPORTE_0002': '2101,00',
    'GXimg_IMPRIMIR_0003': 'bigfolder.gif',
    '_COBNRO_0003': '508995783',
    '_FECHA_0003': '14/06/2021',
    '_IMPORTE_0003': '2101,00',
    'GXimg_IMPRIMIR_0004': 'bigfolder.gif',
    '_COBNRO_0004': '509204456',
    '_FECHA_0004': '14/08/2021',
    '_IMPORTE_0004': '2182,00',
    'GXimg_IMPRIMIR_0005': 'bigfolder.gif',
    '_COBNRO_0005': '509296678',
    '_FECHA_0005': '18/10/2021',
    '_IMPORTE_0005': '2182,00',
    'GXimg_IMPRIMIR_0006': 'bigfolder.gif',
    '_COBNRO_0006': '509374168',
    '_FECHA_0006': '11/12/2021',
    '_IMPORTE_0006': '2182,00',
    'nRC_Grillacobros': '6',
    'sCallerURL': '',
    '_TODAY': '2022-09-30',
  }

  response = request_imc('post', 'himprimirduplicadoperiodo', data)
  match = re.findall(r'href=["]?javascript:miVentana_Encript\(([^" >]+)["]?', response.text)
  download_invoice_url = match[0].split(',')[0].replace('\'', '')

  response = request_imc('get', download_invoice_url)

  file_path = f'pdfs/copy_{_id}_{year}_{invoice_id}.pdf'
  open(file_path, 'wb').write(response.content)

def request_imc(method, path, data={}):
  imc_url = 'https://tributos.imcanelones.gub.uy:8443/cows/servlet/'
  url = imc_url + path
  
  cookies = {
    'GX_SESSION_ID': 'yc3pgQrDDoqd0skF0%2B8F%2FrvpZZ4cKCYBwIQom7rRGrM%3D',
    'JSESSIONID': '5D3F3E6F9D29ED953451CECBE1474BF5',
    '_fbp': 'fb.2.1663724475802.786148759',
    '_ga': 'GA1.3.1227441019.1663724478',
  }

  headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'GX_SESSION_ID=yc3pgQrDDoqd0skF0%2B8F%2FrvpZZ4cKCYBwIQom7rRGrM%3D; JSESSIONID=5D3F3E6F9D29ED953451CECBE1474BF5; _fbp=fb.2.1663724475802.786148759; _ga=GA1.3.1227441019.1663724478',
    'Origin': 'https://tributos.imcanelones.gub.uy:8443',
    'Referer': url,
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
  }

  if method == 'post':
    return requests.post(url, cookies=cookies, headers=headers, data=data, verify=False)
  else:
    return requests.post(url, cookies=cookies, headers=headers, verify=False)

