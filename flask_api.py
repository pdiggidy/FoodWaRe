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
args.add_argument("barcode", type=str, help="barcode number")
args.add_argument("id", type=str)
args.add_argument("key", type=str, required=True)
args.add_argument("quantity", type=int)


def update_values(old, new, barcode):
    first = False
    try:
        old = old[0]
    except IndexError as e:
        first = True
    if not first:
        id_dicts = []
        for i in old:
            id_dicts.append(json.loads(i))
        found = False
        for item in id_dicts:
            if item["id"] == new["id"] and item["quantity"] == new["quantity"]:
                item["certainty"] = item["certainty"] + 1
                found = True
                break
        if not found:
            id_dicts.append((new | {"certainty": 1}))
            return f'''UPDATE barcodes SET id={id_dicts} WHERE barcode={barcode}'''
    elif first:
        id_dicts = new | {"certainty": 1}
        return f'''INSERT INTO barcodes (barcode, id) VALUES ({barcode}, "{id_dicts}")'''


class ProductInfo(Resource):
    def post(self):
        arg = args.parse_args()
        if arg["key"] == key.key:

            conn = psycopg2.connect(DATABASE_URL, sslmode="require")
            cur = conn.cursor()

            cur.execute(f'SELECT id FROM barcodes WHERE barcode={int(arg["barcode"])}')
            ids = dict()
            data = cur.fetchall()
            new = {"id": arg["id"], "quantity": arg["quantity"]}
            query = update_values(data, new, arg["barcode"])
            # try:
            #     id_dict = {arg["id"]: 1}
            #     if arg["quantity"] is not None:
            #         cur.execute(
            #             f'''INSERT INTO barcodes (barcode, id, quantity) VALUES ({int(arg["barcode"])},'{json.dumps(id_dict)}', {arg["quantity"]})''')
            #     else:
            #         cur.execute(
            #             f'''INSERT INTO barcodes (barcode, id) VALUES ({int(arg["barcode"])},'{json.dumps(id_dict)}')''')
            #     conn.commit()
            #     conn.close()
            #     return {"barcode": arg['barcode'], "id": arg["id"], "quantity": arg["quantity"]}, 200
            # except:
            #     conn.commit()
            #     for s in data:
            #         s = json.loads(s[0])
            #         ids[list(s.keys())[0]] = list(s.values())[0]
            #     try:
            #         ids[str(arg["id"])] = ids[str(arg["id"])] + 1
            #     except KeyError as e:
            #         ids[str(arg["id"])] = 1
            #     query = f'''UPDATE barcodes SET id='{json.dumps(ids)}' WHERE barcode = {int(arg["barcode"])}'''
            cur.execute(query)
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
    barcode = int(barcode)
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
    id_list = [f'{{"{k}":{value}}}' for k, value in ids.items()]
    id_list = [json.loads(x) for x in id_list]
    conn.close()
    return {"barcode": barcode, "products": id_list, "quantity": amount}, 200


if __name__ == "__main__":
    # print(db)
    app.run(debug=True)
    # db.to_pickle("fresh_dataframe.pickle")
