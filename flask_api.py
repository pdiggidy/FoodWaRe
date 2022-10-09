import flask
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
args.add_argument("key", type=int, required=True)


class ProductInfo(Resource):
    def get(self):
        arg = args.parse_args()
        if True:  # sha256(arg["key"]) == key.key:
            conn = sqlite3.connect("Barcodes.sql")
            cur = conn.cursor()

            data = cur.execute(f'SELECT * FROM barcodes WHERE barcode = {int(arg["barcode"])}')
            products = data.fetchall()
            products=list(products)[0]
            conn.close()
            try:
                return {'barcode': arg["barcode"], "products": {"id": products[2], "certainty": products[3]}}, 200
            except IndexError as e:
                return "broken"
                conn.close()
                abort(400)

        else:
            abort(401)

    def post(self):
        arg = args.parse_args()
        if True:  # (sha256(arg["key"]) == secrets.key):

            conn = sqlite3.connect("Barcodes.sql")
            cur = conn.cursor()

            data = cur.execute(f'SELECT * FROM barcodes WHERE barcode={arg["barcode"]}')
            try:
                info = data.fetchall()[0]
                id_str = info[2]
                cert = info[3]
                if id_str == info[2]:
                    cert = int(cert) + 1
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
    return "test"


if __name__ == "__main__":
    # print(db)
    app.run(debug=True)
    # db.to_pickle("fresh_dataframe.pickle")
