from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, reqparse, http_status_message
import pandas as pd

db = pd.read_pickle("cleaned_food.pickle")

app = Flask(__name__)
api = Api(app)

args = reqparse.RequestParser()
args.add_argument("barcode", type=int, help="barcode number")
args.add_argument("id", type=str)


class ProductInfo(Resource):
    def get(self):
        arg = args.parse_args()
        try:
            products = db.loc[db["code"]==int(arg["barcode"])][["code","categories_en","certainty"]]
            return {'barcode': arg["barcode"], "products" : products.to_dict('r')}, 200
        except KeyError as e:
            abort(400)


    def post(self):
        arg = args.parse_args()
        return {"barcode": arg["barcode"], "id":arg["id"]}


api.add_resource(ProductInfo, "/api/v1")

if __name__ == "__main__":
    app.run(debug=True)
