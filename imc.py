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

def get_debt(id):
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
      'Referer': 'https://tributos.imcanelones.gub.uy:8443/cows/servlet/hconsultadeudawebcan',
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

  data = {
      '_EventName': 'E\'CONSULTA DE DEUDA\'.',
      '_EventGridId': '20',
      '_EventRowId': '1',
      '_IDPADRON': id,
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

  response = requests.post('https://tributos.imcanelones.gub.uy:8443/cows/servlet/hconsultadeudawebcan', cookies=cookies, headers=headers, data=data, verify=False)

  obj = PyQuery(response.text)
  message = obj('span#span__MENSAJERETORNO').text()
  debt = obj('span#span__MONTOFINAL_0001').text()
  debt = float(debt.replace('.', '').replace(',','.'))

  print(message)
  print(debt)

  if message == constants.NOT_FOUND_MSG:
    return constants.NOT_FOUND
  
  if message == constants.NO_DEBT_MSG:
    return constants.NO_DEBT

  if debt > 0:
    return constants.IN_DEBT
