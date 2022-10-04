from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, reqparse, http_status_message
import pandas as pd

db = pd.read_pickle("fresh_dataframe.pickle")

app = Flask(__name__)
api = Api(app)

args = reqparse.RequestParser()
args.add_argument("barcode", type=int, help="barcode number")
args.add_argument("id", type=str)


class ProductInfo(Resource):
    def get(self):
        arg = args.parse_args()
        try:
            products = db.loc[db["barcode"]==int(arg["barcode"])][["barcode","id","certainty"]]
            return {'barcode': arg["barcode"], "products" : products.to_dict('r')}, 200
        except KeyError as e:
            abort(400)


    def post(self):
        arg = args.parse_args()
        if arg["barcode"] in db["barcode"]:
            if arg["id"] in db.loc["barcode","id"]:
                cert = db.loc["barcode","certainty"]
                cert[db.loc["barcode", "id"].index(arg["id"])] = cert[db.loc["barcode", "id"].index(arg["id"])] +1
                db.loc["barcode", "certainty"] = cert
        else:
            pd.concat([db,pd.DataFrame({"barcode":[arg["barcode"]],"id":[arg["id"]],"certainty":[1]})])
        return {"barcode": arg["barcode"], "id":arg["id"]}


api.add_resource(ProductInfo, "/api/v1")

if __name__ == "__main__":
    print(db)
    app.run(debug=True)
    db.to_pickle("fresh_dataframe.pickle")
