from helpers import db

db.put("AMARA:buy", "134")

print(db.get("AMARA:buy"))

db.put("AMARA:sell", "123")

print(db.get("AMARA:sell"))
db.put("AMARA:sell", "1232")
print(db.get("AMARA:sell"))