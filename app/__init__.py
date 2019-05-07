import os
from .utils.ml import MLProcess
from flask import Flask, current_app, send_file, jsonify, request

from .api import api_bp
from .client import client_bp
import pandas as pd

app = Flask(__name__, static_folder='../dist/static')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024
app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)

savedata = None

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@app.route('/api/uploadfile', methods=["POST"])
def fileupload():
  try:
    file = request.files['file']
    _HERE = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(_HERE, "logs")
    if not os.path.exists(path):
      os.makedirs(path)
    # save(f, os.path.join(path, f.filename))
    ml = MLProcess(file)
    data = ml.getResult()
    savedata = ml.getCSV()
    # data = pd.read_csv(os.path.join(path, 'dataset.csv'))
    # return jsonify({"data": data.to_json(orient='records')})
    return jsonify({"data": data})
  except:
    return jsonify({"done": False})

@app.route('/api/download/<ip>', methods=["GET"])
def download(ip=None):
  try:
    return send_file(savedata.to_csv(index=False))
  except expression as identifier:
    pass