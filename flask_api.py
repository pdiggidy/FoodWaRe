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

DATABASE_URL = "postgres://fwahrxcyduwmlg:a7b249158e16deb53ce3127fa7f713ecb2264d29eaf0ddd2cdda0a89eb84dde4@ec2-176-34-215-248.eu-west-1.compute.amazonaws.com:5432/d15j4vkuqikc2c"

# conn = psycopg2.connect(DATABASE_URL, sslmode="require")
# cur = conn.cursor()

args = reqparse.RequestParser()
args.add_argument("barcode", type=int, help="barcode number")
args.add_argument("id", type=str)
args.add_argument("key", type=str, required=True)
args.add_argument("quantity", type=int)


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
        if arg["key"] == key.key:

            conn = psycopg2.connect(DATABASE_URL, sslmode="require")
            cur = conn.cursor()

            cur.execute(f'SELECT id FROM barcodes WHERE barcode={arg["barcode"]}')
            ids = dict()

            try:
                for s in cur.fetchall():
                    s = json.loads(s[0])
                    ids[list(s.keys())[0]] = list(s.values())[0]
                try:
                    ids[str(arg["id"])] = ids[str(arg["id"])] + 1
                except KeyError as e:
                    ids[str(arg["id"])] = 1
                    query = f'''UPDATE barcodes SET id='{json.dumps(ids)}' WHERE barcode = {arg["barcode"]}'''
                cur.execute(query)
                conn.commit()
                conn.close()
                return {"barcode": arg['barcode'], "id": arg["id"], "quantity": arg["quantity"]}, 200
            except:
                id_dict = {arg["id"]: 1}
                if arg["quantity"] is not None:
                    cur.execute(
                        f'''INSERT INTO barcodes (barcode, id, quantity) VALUES ({arg["barcode"]},'{json.dumps(id_dict)}', {arg["quantity"]})''')
                else:
                    cur.execute(
                        f'''INSERT INTO barcodes (barcode, id) VALUES ({arg["barcode"]},'{json.dumps(id_dict)}')''')
                conn.commit()
                conn.close()
                return {"barcode": arg['barcode'], "id": arg["id"], "quantity": arg["quantity"]}, 200

        else:
            abort(401)


api.add_resource(ProductInfo, "/api/v1")


@app.route('/')
def hello():
    return "test"


@app.route('/api/v1/products/<int:barcode>')
def barcode_info(barcode):
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()

    cur.execute(f'SELECT id, quantity FROM barcodes WHERE barcode = {barcode}')
    products = cur.fetchall()
    try:
        products = list(products)[0]
    except IndexError as e:
        conn.close()
        return "Barcode does not exist", 400
    ids = {}
    try:
        s = json.loads(products[0])
        ids[list(s.keys())[0]] = list(s.values())[0]
    except json.JSONDecodeError as e:
        return f"Broken, Data: {cur.fetchall()}"
    amount = products[1]
    id_list = [f'{{{k}:{value}}}' for k, value in ids.items()]
    conn.close()
    return {"barcode": barcode, "products": json.dumps(id_list), "quantity": amount}, 200


if __name__ == "__main__":
    # print(db)
    app.run(debug=True)
    # db.to_pickle("fresh_dataframe.pickle")
