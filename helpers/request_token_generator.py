from urllib.parse import urlparse, parse_qs

from kiteconnect import KiteConnect

kite = KiteConnect(api_key="tf77pivddr8pmyin")

file = open("request_token.txt", "w")

url = 'http://127.0.0.1:19291/kite-redirect?type=login&status=success&request_token=88dI425RwXrqrBh4vmC83hlQTUWjUbHk&action=login'
parsed_url = urlparse(url)
captured_value = parse_qs(parsed_url.query)['request_token'][0]

data = kite.generate_session(captured_value, api_secret="pol1gkoy18dx1x3qa9xdyvs3er3cxxe4")
file.write(data["access_token"])
print("Request token generated", data)
