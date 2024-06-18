import scrap
import data_base
import report



collection  = data_base.connection_db()
for ci in ["Bordeaux","Paris","Rennes"]:
    data = scrap.scrap_offers(ci)
    resp = data_base.insert_data(data,collection)
report.report(collection)