from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, reqparse, http_status_message
import pandas as pd
import sqlite3
from hashlib import sha256
import key


app = Flask(__name__)
api = Api(app)

args = reqparse.RequestParser()
args.add_argument("barcode", type=int, help="barcode number")
args.add_argument("id", type=str)
args.add_argument("key",type=int, required=True)


class ProductInfo(Resource):
    def get(self):
        arg = args.parse_args()
        if True:#sha256(arg["key"]) == key.key:
            conn = sqlite3.connect("Barcodes.sql")
            cur = conn.cursor()

            data = cur.execute(f'SELECT * FROM barcodes WHERE barcode = "871039852411"')
            products = data.fetchall()
            return_payload = []
            for prod in products:
                return_payload.append({"barcode": prod[1], "id": prod[2], "certainty":prod[3]})
            conn.close()
            try:
                return {'barcode': arg["barcode"] , "products":[{"barcode": prod[1], "id": prod[2], "certainty":prod[3]} for prod in products]}, 200
            except KeyError as e:
                conn.close()
                abort(400)

        else:
            abort(401)

    def post(self):
        arg = args.parse_args()
        if True:#(sha256(arg["key"]) == secrets.key):
            ##TODO: CHANGE THIS TO SQL QUERY
            ##TODO: ADD SHA AUTH
            if arg["barcode"] in db["barcode"]:
                if arg["id"] in db.loc["barcode","id"]:
                    cert = db.loc["barcode","certainty"]
                    cert[db.loc["barcode", "id"].index(arg["id"])] = cert[db.loc["barcode", "id"].index(arg["id"])] +1
                    db.loc["barcode", "certainty"] = cert
            else:
                pd.concat([db,pd.DataFrame({"barcode":[arg["barcode"]],"id":[arg["id"]],"certainty":[1]})])
            return {"barcode": arg["barcode"], "id":arg["id"]}
        else:
            abort(401)

api.add_resource(ProductInfo, "/api/v1")

if __name__ == "__main__":
    #print(db)
    app.run(debug=True)
    #db.to_pickle("fresh_dataframe.pickle")
