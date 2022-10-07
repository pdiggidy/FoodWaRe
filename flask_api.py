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

            data = cur.execute(f'SELECT * FROM barcodes WHERE barcode = {str(arg["barcode"])}')
            products = data.fetchall()
            return_payload = []
            for prod in products:
                return_payload.append({"barcode": prod[1], "id": prod[2], "certainty":prod[3]})
            conn.close()
            try:
                return {'barcode': arg["barcode"], "products":[{"barcode": prod[1], "id": prod[2], "certainty":prod[3]} for prod in products]}, 200
            except IndexError as e:
                conn.close()
                abort(400)

        else:
            abort(401)

    def post(self):
        arg = args.parse_args()
        if True:#(sha256(arg["key"]) == secrets.key):
            ##TODO: CHANGE THIS TO SQL QUERY
            ##TODO: ADD SHA AUTH

            conn = sqlite3.connect("Barcodes.sql")
            cur = conn.cursor()

            data = cur.execute(f'SELECT * FROM barcodes WHERE barcode={arg["barcode"]}')
            try:
                info = data.fetchall()[0]
                id_str = info[2]
                cert = info[3]
                if str(arg["id"]) in id_str.split(","):
                    split_cert = [int(x) for x in str(cert).split(",")]
                    split_id = [int(y) for y in id_str.split(",")]
                    split_cert[split_id.index(int(arg["id"]))] = split_cert[split_id.index(int(arg["id"]))] + 1
                    cert = ','.join(map(str, split_cert))

                else:
                    id_str = id_str + f",{str(arg['id'])}"
                    cert = cert + ",1"
                cur.execute(f'UPDATE barcodes SET id={id_str}, certainty={cert} WHERE barcode = {str(arg["barcode"])}')
                conn.commit()
                conn.close()
                return {"barcode": arg['barcode'], "id": arg["id"]}, 200
            except IndexError as e:
                cur.execute(f'INSERT INTO barcodes (barcode, id, certainty) VALUES ({arg["barcode"]},{arg["id"]},1)')
                conn.commit()
                conn.close()
                return {"barcode": arg['barcode'], "id": arg["id"]}, 200

        else:
            abort(401)

api.add_resource(ProductInfo, "/api/v1")

@app.route('/')
def hello():
    return """<!DOCTYPE html>
           <embed src="Api Version 1 specification.pdf" width="100%" height="800px" /> """

if __name__ == "__main__":
    #print(db)
    app.run(debug=True)
    #db.to_pickle("fresh_dataframe.pickle")
