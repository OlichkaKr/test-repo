import base64
import urllib.request

from flask import Flask, json, request
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
# app.config['MONGO_URI'] = "mongodb://oilproductioninfo:GtPvmWddBMjnLCLTvgPETffWGg5ENcDJZg4mSqmmiiiaxyME3DNR3vpwrwaAvqeTV0yTx8XNBTBqtDTWg0PuCw==@oilproductioninfo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
# mongo = PyMongo(app)
client = MongoClient("mongodb://oilproductioninfo.documents.azure.com:10255/?ssl=true")
db = client.test
db.authenticate(name="oilproductioninfo",password="GtPvmWddBMjnLCLTvgPETffWGg5ENcDJZg4mSqmmiiiaxyME3DNR3vpwrwaAvqeTV0yTx8XNBTBqtDTWg0PuCw==")


@app.route("/")
def hello():
    return 'Hello'


@app.route("/api/service/get/all", methods=['GET'])
def get_all_data():
    test = db.test
    data = list(test.find({}))
    result_data = {}
    for key, value in enumerate(data):
        result_data[key] = dict(list(value.items())[1:])
        result_data[key]['image'] = base64.b16encode(result_data[key]['image'])
    # or via dict comprehension
    # result_data = {i: dict(list(data[i].items())[1:]) for i in range(len(data))}
    return json.dumps(result_data)


@app.route("/api/service/post", methods=['GET', 'POST'])
def post_data():
    test = db.test
    data = request.form['data']
    encoded_string = ''
    urllib.request.urlretrieve('https://image.freepik.com/free-vector/_1378-197.jpg', 'image.bmp')
    with open("image.bmp", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = json.loads(data)
    data['image'] = encoded_string
    test.insert(data)
    d = list(test.find({}))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

