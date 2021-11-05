from helpers import db
#
# db.put("AMARA:buy", "134")
#
# print(db.get_price("AMARA:buy"))
#
# db.put("AMARA:sell", "123")
#
# print(db.get_price("AMARA:sell"))
# db.put("AMARA:sell", "1232.2")
# print(db.get_price("AMARA:sell"))


from helpers.db import log_todays_entries

log_todays_entries()