import requests as req
import json
import pandas as pd

# db = pd.read_pickle("cleaned_food.pickle")
#
# test = db.head()
# def s(str):
#     return str.split(",")
# db["categories_en"] = db["categories_en"].apply(s)
# db.to_pickle("cleaned_food.pickle")


print(req.post("http://127.0.0.1:5000/api/v1", data=json.dumps({"barcode": 26772226, "id":"1"}), headers={'content-type': 'application/json'}).text)
# print(req.get("http://127.0.0.1:5000/api/v1", data=json.dumps({"barcode": 26772226}), headers={'content-type': 'application/json'}).json())
#
# d= {"barcode":[871039852411],"id":["17"],"certainty":[1]}
# test_db = pd.DataFrame(d)
#
# test_db.to_pickle("fresh_dataframe.pickle")