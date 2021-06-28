import os
from flask_cors import CORS, cross_origin
from flask import request
from flask import Flask


app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/upload', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        print('------------------------', request.files)
        print('+++++++++++++++++++++++++', request.files['file'])
        f = request.files['file']
        f.save('./files/uploaded_file.txt')
    else:
        return 'GET UPLOAD'


@app.route('/deneme', methods=['GET', 'POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        if valid_data(request.form['user_stories']):
            return post_is_true()
        else:
            return post_is_false()
    else:
        return do_the_get()


def post_is_false():
    return 'File is FALSE'


def post_is_true():
    return 'File is TRUE'


def do_the_get():
    return 'Selam GET'


def valid_data(data_file):
    f = os.listdir(data_file)
    if len(f) > 0:
        for i in os.listdir(data_file):
            if i.endswith('.txt'):
                return True
            else:
                return False
