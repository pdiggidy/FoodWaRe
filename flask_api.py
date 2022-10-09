import flask
from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, reqparse, http_status_message
import pandas as pd
import sqlite3
from hashlib import sha256
import key
import json
import os
import psycopg2

app = Flask(__name__)
api = Api(app)

args = reqparse.RequestParser()
args.add_argument("barcode", type=int, help="barcode number")
args.add_argument("id", type=str)
args.add_argument("key", type=int, required=True)


class ProductInfo(Resource):
    # def get(self):
    #     arg = args.parse_args()
    #     if True:  # sha256(arg["key"]) == key.key:
    #         conn = sqlite3.connect("Barcodes.sql")
    #         cur = conn.cursor()
    #
    #         data = cur.execute(f'SELECT * FROM barcodes WHERE barcode = {int(arg["barcode"])}')
    #         products = data.fetchall()
    #         products=list(products)[0]
    #         conn.close()
    #         try:
    #             return {'barcode': arg["barcode"], "products": {"id": products[2], "certainty": products[3]}}, 200
    #         except IndexError as e:
    #             return "broken"
    #             conn.close()
    #             abort(400)
    #
    #     else:
    #         abort(401)

    def post(self):
        arg = args.parse_args()
        if True:  # (sha256(arg["key"]) == secrets.key):

            conn = sqlite3.connect("Barcodes.sql")
            cur = conn.cursor()

            data = cur.execute(f'SELECT id FROM barcodes WHERE barcode={arg["barcode"]}')
            ids = dict()
            if len(data.fetchall()) == 0:
                id_dict = {arg["id"]:1}
                cur.execute(f'INSERT INTO barcodes (barcode, id, certainty) VALUES ({arg["barcode"]},{json.dumps(id_dict)})')
                conn.commit()
                conn.close()
                return {"barcode": arg['barcode'], "id": arg["id"]}, 200

            for s in data.fetchall():
                s = json.loads(s[0])
                ids[list(s.keys())[0]]= list(s.values())[0]
            try:
                ids[str(arg["id"])] = ids[str(arg["id"])]+1
            except KeyError as e:
                ids[str(arg["id"])] = 1
            query = f'''UPDATE barcodes SET id='{json.dumps(ids)}' WHERE barcode = {str(arg["barcode"])}'''
            cur.execute(query)
            conn.commit()
            conn.close()
            return  {"barcode": arg['barcode'], "id": arg["id"]}, 200

        else:
            abort(401)


api.add_resource(ProductInfo, "/api/v1")


@app.route('/')
def hello():
    return "test"


@app.route('/api/v1/products/<int:barcode>')
def barcode_info(barcode):
    if True:  # sha256(arg["key"]) == key.key:
        conn = sqlite3.connect("Barcodes.sql")
        cur = conn.cursor()

        data = cur.execute(f'SELECT id FROM barcodes WHERE barcode = {barcode}')
        products = data.fetchall()
        try:
            products = list(products)[0]
        except IndexError as e:
            conn.close()
            return "Barcode does not exist", 400
        ids = {}
        for s in products:
            try:
                s = json.loads(s)
                ids[list(s.keys())[0]] = list(s.values())[0]
            except json.JSONDecodeError as e:
                return s
        #id_list = [f'{{{k}}}:{value}' for k, value in ids.items()]
        conn.close()
        return {"barcode": barcode, "products": json.dumps(ids)}, 200


if __name__ == "__main__":
    # print(db)
    app.run(debug=True)
    # db.to_pickle("fresh_dataframe.pickle")
