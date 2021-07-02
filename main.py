import os
from flask_cors import CORS, cross_origin
from flask import request
from flask import Flask
from flask import jsonify
from preprocess import all_functions
from neo_db import create_graph
from neo_db import get_nodes_specific


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
        f = request.files['file']
        if f.filename.endswith('.txt'):
            f.save('./files/uploaded_file.txt')
            all_functions()
            create_graph()
            return jsonify('File succesfully uploaded.')
        else:
            return jsonify('Please upload txt file.')

    else:
        return jsonify('GET UPLOAD')


@app.route("/nodes", methods=['GET'])
@cross_origin()
def get_nodes():
    whichNode = request.headers['node']
    my_list = get_nodes_specific(whichNode)
    print('----------------', my_list)
    return jsonify({"Nodes": my_list})
