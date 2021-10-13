from urllib.parse import urlparse, parse_qs

from kiteconnect import KiteConnect

kite = KiteConnect(api_key="tf77pivddr8pmyin")

token_file = open("token.txt", "r")

file = open("request_token.txt", "w")

url = token_file.readline()
parsed_url = urlparse(url.strip())
captured_value = parse_qs(parsed_url.query)['request_token'][0]
print("Request_token", captured_value.strip())
data = kite.generate_session(captured_value, api_secret="pol1gkoy18dx1x3qa9xdyvs3er3cxxe4")
file.write(data["access_token"])
print("Request token generated", data)
