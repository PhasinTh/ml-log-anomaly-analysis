import os
from flask import Flask, current_app, send_file, jsonify, request

from .api import api_bp
from .client import client_bp
import pandas as pd
import json
from collections import OrderedDict

import geoip2.database
from geoip2.errors import AddressNotFoundError

import time

# from keras.preprocessing import sequence
# from keras.models import load_model

import re
from joblib import dump, load

from urllib.parse import urlparse, parse_qs

app = Flask(__name__, static_folder='../dist/static')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024
app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

here = os.path.dirname(os.path.abspath(__file__))

def getCountry(ip):
  try:
    reader_country = geoip2.database.Reader(os.path.join(here, 'utils/GeoLite2-Country.mmdb'))
    return reader_country.country(ip).country.iso_code
  except AddressNotFoundError :
    return 'N/a'
    pass

def parse(data, pattern):
  for count, line in enumerate(data.split('\n')):
    line = line.strip()
    if line:
      match = pattern.match(line)
      if not match:
        pattern = build_pattern(autoformat(line))
        match = pattern.match(line)

      if match:
        item = match.groupdict()
        item['status'] = int(item['status'])
        if item['bytes'].isnumeric():
          item['bytes'] = int(item['bytes'])
        else:
          item['bytes'] = 0
        # if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",item['remote_addr']):
        #   # print('pass')
        #   country = getCountry(str(item['remote_addr']))
        #   item['country'] = country if country else 'N/a'
        # else:
        #   item['country'] = 'N/a'
        match = re.match('^(\w+)\s+(.*?)\s+(.*?)$', str(item['request']))
        if match:
          item['method'], item['path'], item['version'] = match.groups()
          del item['request']
        else:
          match = re.match('^(\w+)\s+(.*?)$', str(item['request']))
          if match:
            item['method'], item['path'] = match.groups()
            item['version'] = '-'
      yield item

def build_pattern(format):
  REGEX_SPECIAL_CHARS = r'([\.\*\+\?\|\(\)\{\}\[\]])'
  REGEX_LOG_FORMAT_VARIABLE = r'\$([a-zA-Z0-9\_]+)'
  pattern = re.sub(REGEX_SPECIAL_CHARS, r'\\\1', format)
  pattern = re.sub(REGEX_LOG_FORMAT_VARIABLE, '(?P<\\1>.*)', pattern)
  return re.compile(pattern)

# def build_model():
#   global model
#   model = load_model(os.path.join(here, "models/rnn-model.h5"))
#   model.load_weights(os.path.join(here, "models/rnn-weights.h5"))
#   model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

def autoformat(test):
  common = '$remote_addr - - [$timestamp] "$request" $status $bytes'
  combine = '$remote_addr - - [$timestamp] "$request" $status $bytes "$refferer" "$user_agent"'
  withcokie = '$remote_addr - - [$timestamp] "$request" $status $bytes "$refferer" "$user_agent" "$cookie"'
  format = ''
  if build_pattern(withcokie).match(test):
    format = withcokie
  elif build_pattern(combine).match(test):
    format = combine
  elif build_pattern(common).match(test):
    format = common
  return format

def predict(x):
  char_vectorizer = load(os.path.join(here,'utils/char_vectorizer'))
  log_entry_processed = char_vectorizer.transform(x)
  clf = load(os.path.join(here,'models/Random Forest.joblib'))
  return clf.predict(log_entry_processed)

@app.route('/')
def index_client():
  dist_dir = current_app.config['DIST_DIR']
  entry = os.path.join(dist_dir, 'index.html')
  return send_file(entry)

@app.route('/api/uploadfile', methods=["POST"])
def fileupload():
  start = time.time()
  file = request.files['file']
  buffer_size=16384
  data = bytearray()
  while 1:
    buff = file.read(buffer_size)
    if not buff:
      break
    data.extend(buff)
  logs = data.decode('utf-8')
  end = time.time()
  print("read file take time {}".format(end - start))

  start = time.time()
  # auto format
  test = logs.split('\n')[0]
  format = autoformat(test)
  end = time.time()
  print("auto format take time {}".format(end - start))

  start = time.time()
  # parser
  pattern = build_pattern(format)
  data = list(parse(logs, pattern))
  end = time.time()
  print("parsing take time {}".format(end - start))

  newlist = [x['path'] for x in data]
  start = time.time()
  pred = predict(newlist)
  end = time.time()
  print("prediction take time {}".format(end - start))
  start = time.time()
  for i in range(len(data)):
    data[i]['line'] = i + 1
    data[i]['class'] = pred[i]
  end = time.time()
  print("labeling take time {}".format(end - start))
  start = time.time()
  df = pd.DataFrame.from_dict(data)
  json = df.to_json(orient='records')
  end = time.time()
  print("json parsing take time {}".format(end - start))
  return jsonify({"data": json})

# @app.route("/api/prediction", methods=["POST"])
# def predict():
#   build_model()
#   data = {"success": False}
#   if request.form['log']:
#     logs = json.loads(request.form['log'])
#     poslog = logs.copy()
#     for index, item in enumerate(logs):
#       X = {}
#       parse = urlparse(item['path'])
#       X['Method'] = item['method']
#       X['Path'] = str(parse.path)
#       X['Status'] = item['status']
#       X['Query'] = str(parse.query) if parse.query else str({})
#       logs[index] = json.dumps(X, separators=(',', ':'))

#     with open(os.path.join(here, 'models/tokenizer.pickle'), 'rb') as handle:
#       ptokenizer = pickle.load(handle)

#     max_log_length = 1024
#     seq = ptokenizer.texts_to_sequences(logs)
#     log_entry_processed = sequence.pad_sequences(seq, maxlen=max_log_length)

#     # from joblib import load
#     # clf = load(os.path.join(here, 'models/Random Forest.joblib'))
#     # pred = clf.predict(log_entry_processed)


#     pred = model.predict_classes(log_entry_processed)

#     for i in range(len(poslog)):
#       poslog[i]['class'] = int(pred[i])
#     # print(log_entry_processed)
#     # prediction = model.predict_classes([log_entry_processed])
#     # print(pred)  
#   return jsonify({"data": json.dumps(poslog)})

