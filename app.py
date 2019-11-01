from flask import Flask, json, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://oilproductioninfo:GtPvmWddBMjnLCLTvgPETffWGg5ENcDJZg4mSqmmiiiaxyME3DNR3vpwrwaAvqeTV0yTx8XNBTBqtDTWg0PuCw==@oilproductioninfo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
mongo = PyMongo(app)


@app.route("/")
def hello():
    return 'Hello'


@app.route("/api/service/get/all", methods=['GET'])
def get_all_data():
    test = mongo.db.test
    data = list(test.find({}))
    result_data = {}
    for key, value in enumerate(data):
        result_data[key] = dict(list(value.items())[1:])
    # or via dict comprehension
    # result_data = {i: dict(list(data[i].items())[1:]) for i in range(len(data))}
    return json.dumps(result_data)


@app.route("/api/service/post", methods=['GET', 'POST'])
def post_data():
    test = mongo.db.test
    data = request.form['data']
    test.insert(json.loads(data))
    d = list(test.find({}))
    return json.dumps({len(d) - 1: data})
