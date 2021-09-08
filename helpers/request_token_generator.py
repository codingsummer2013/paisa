from kiteconnect import KiteConnect

kite = KiteConnect(api_key="tf77pivddr8pmyin")

file = open("request_token.txt", "w")
data = kite.generate_session("JM9OoOf35x88zBmEWX9iOrPRmftzj39t", api_secret="pol1gkoy18dx1x3qa9xdyvs3er3cxxe4")
file.write(data["access_token"])
print("Request token generated", data)
