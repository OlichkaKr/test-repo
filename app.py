
import base64
import urllib.request

from flask import Flask, json, request
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
db_ref = db.collection('akerbr')


@app.route("/")
def hello():
    return 'Hello'


@app.route("/api/service/get/all", methods=['GET'])
def get_all_data():
    data = [doc.to_dict() for doc in db_ref.stream()]
    result_data = {}
    for key, value in enumerate(data):
        result_data[key] = dict(list(value.items()))
        # result_data[key]['image'] = base64.b16decode(result_data[key]['image'])
    # or via dict comprehension
    # result_data = {i: dict(list(data[i].items())[1:]) for i in range(len(data))}
    return json.dumps(result_data)


@app.route("/api/service/post", methods=['GET', 'POST'])
def post_data():
    data = request.form['data']
    encoded_string = ''
    urllib.request.urlretrieve('https://image.freepik.com/free-vector/_1378-197.jpg', 'image.bmp')
    with open("image.bmp", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    data = json.loads(data)
    data['image'] = encoded_string
    db_ref.document().set(data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/api/service/post/android", methods=['POST'])
def post_from_android():
    query_parameters = request.args.get()
    # cords = query_parameters.get('cords')
    # filling = query_parameters.get('filling')
    # export = query_parameters.get('export')
    # image = query_parameters.get('image')
    # data = json.loads({'image': image, 'cords': cords, 'filling': filling, 'export': export})
    db_ref.document().set(query_parameters)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
