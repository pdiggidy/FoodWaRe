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


barcode= 871039852411
#print(req.get(f"https://foodware-backend.herokuapp.com/api/v1/products/1111").json())#, data=json.dumps({"barcode": 871039852411, "key": 1}), headers={'content-type': 'application/json'}).json())

print(req.post("https://foodware-backend.herokuapp.com//api/v1", data=json.dumps({"barcode": "1111", "id":"5","quantity":100, "key":"27b7ad855cbc541a83b45b657ac7fdc8b10f19f0c6b028a854322f6e0a8e43e4"}), headers={'content-type': 'application/json'}).text)
#print(req.post("http://127.0.0.1:5000/api/v1", data=json.dumps({"barcode": 871039852411, "key": 1, "id":17, "quantity":100}), headers={'content-type': 'application/json'}).json())
#
# d= {"barcode":[871039852411],"id":["17"],"certainty":[1]}
# test_db = pd.DataFrame(d)
#
# test_db.to_pickle("fresh_dataframe.pickle")

#curl -X POST https://foodware-backend.herokuapp.com/api/v1 -H "Content-Type: application/json" -d "{\"barcode\":871039852411,\"key\":1, \"id\":17}
#curl -X GET https://foodware-backend.herokuapp.com/api/v1 -H "Content-Type: application/json" -d "{\"barcode\":871039852411,\"key\":1, \"id\":17}
#print(req.get("http://127.0.0.1:5000/api/v1/products/871039852411").text)
