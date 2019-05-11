import time
import pandas as pd
import numpy as np
import os
import re
from ua_parser import user_agent_parser
import geoip2.database
from geoip2.errors import AddressNotFoundError
from urllib.parse import urlparse,parse_qs
import json
from sklearn.ensemble import IsolationForest
from joblib import dump, load

# from .logparser import LogParser as logparser

class MLProcess(object):
  def __init__(self, file):
    start = time.time()
    self.file = file
    self.data = self.loadata()
    self.format = self.autoformat()
    self.pattern = self.build_pattern(self.format)
    print(self.pattern)
    self.here = os.path.dirname(os.path.abspath(__file__))
    # self.reader_country = geoip2.database.Reader(os.path.join(self.here, "GeoLite2-Country.mmdb"))
    self.parsedata = list(self.parse(self.data, self.pattern))
    self.features = self.preprocess(self.parsedata)
    self.country = {}

  def autoformat(self):
    test = self.data.split('\n')[0]
    common = '$remote_addr - - [$timestamp] "$request" $status $bytes'
    combine = '$remote_addr - - [$timestamp] "$request" $status $bytes "$refferer" "$user_agent"'
    withcokie = '$remote_addr - - [$timestamp] "$request" $status $bytes "$refferer" "$user_agent" "$cookie"'
    if self.build_pattern(withcokie).match(test):
      return withcokie
    elif self.build_pattern(combine).match(test):
      return combine
    elif self.build_pattern(common).match(test):
      return common
    return None
  
  def getResult(self):
    # print(self.features[0])
    # print(self.parsedata)
    # return self.prediction()
    return self.prediction()
    # return self.load()
  
  def load(self):
    _HERE = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(_HERE, "../logs")
    return pd.read_csv(os.path.join(path, 'dataset.csv')).to_json(orient='records')

  def loadata(self, buffer_size=16384):
    data = bytearray()
    while 1:
      buff = self.file.read(buffer_size)
      if not buff:
        break
      data.extend(buff)
    logs = data.decode('utf-8')
    return logs
  
  def get_country(self, ip):
    return self.reader_country.country(ip).country.iso_code
  
  def build_pattern(self, log_format):
    REGEX_SPECIAL_CHARS = r'([\.\*\+\?\|\(\)\{\}\[\]])'
    REGEX_LOG_FORMAT_VARIABLE = r'\$([a-zA-Z0-9\_]+)'
    pattern = re.sub(REGEX_SPECIAL_CHARS, r'\\\1', log_format)
    pattern = re.sub(REGEX_LOG_FORMAT_VARIABLE, '(?P<\\1>.*)', pattern)
    return re.compile(pattern)
  
  def parse(self, data, pattern):
    for count, line in enumerate(data.split('\n')):
      line = line.strip()
      if line:
        try:
          match = pattern.match(line)
          if match:
            item = match.groupdict()
            item['status'] = int(item['status'])
            item['bytes'] = int(item['bytes'])
            match = re.match('^(\w+)\s+(.*?)\s+(.*?)$', str(item['request']))
            if match:
              item['method'], item['path'], item['version'] = match.groups()
              del item['request']
          else:
            print('err',line)
          yield item
        except:
          print('err',line)

          # print(self.get_country(item['remote_addr']))
        # if item['remote_addr'] in self.country:
        #   item['country'] = self.country[item['remote_addr']]
        # else:
        #   new_country = self.get_country(item['remote_addr'])
        #   item['country'] = new_country
        #   self.country[item['remote_addr']] = new_country
        
        

  # status class = [200, 300, 400, 500]
  def fill_status(self, x):
      status = [200, 206, 301, 302, 400, 404, 500, 'OTHER']
      temp = [0] * 8
      if x in status:
          temp[status.index(x)] = 1
      else:
          temp[len(status) - 1] = 1
      return temp

  # methods class = ['GET', 'POST', 'HEAD', 'OPTIONS', 'OTHER']
  def fill_method(self, x):
    methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'OTHER']
    temp = [0] * 5
    if x in methods:
      # print(methods.index(x))
      temp[methods.index(x)] = 1
    else:
      temp[len(methods) - 1] = 1
    return temp

  # log with safe divide by zero
  def safelog(self, x):
    if x > 0:
      return np.log(x)
    else:
      return 0

  def preprocess(self, items):
    # print('template {}'.format(items[0]))
    features = []
    for _ in items:
      try:
        # categories feature (status, method)
        status = self.fill_status(_['status'])
        httpmethod = self.fill_method(_['method'])
        # numerical feature (bytes, len(url), len(query))
        bodybytes = self.safelog(_['bytes'])
        parseurl = urlparse(_['path'])
        path = self.safelog(len(parseurl.path))
        query = self.safelog(len(parseurl.query))
  #             lenpath = safelog(_['path'])
  #         if query == 0:
  #             print('path: {} query {} : len {}'.format(_['path'],parseurl.query,query))
        features.append(status+httpmethod+[bodybytes,path,query])
      except:
        pass
    return features
  
  def getLogs(self):
    temp = self.parsedata
    for i in range(len(temp)):
      temp[i]['line'] = i + 1
    data = pd.DataFrame.from_dict(temp)
    return data.to_json(orient='records')

  def prediction(self):
    # print(self.parsedata[0])
    # rng = np.random.RandomState(42)
    # clf = IsolationForest(random_state=rng, n_estimators=10, behaviour="new", contamination="auto")
    # print("Start Fit Model")
    # print(features.shape)
    # clf.fit(self.features)
    # print("Done Fit Model")
    _HERE = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(_HERE, "Random Forest.joblib")
    clf = load(path)
    predicts = clf.predict(self.features)
    print("Done prediction")
    for i in range(len(self.parsedata)):
      self.parsedata[i]['line'] = i+1
      self.parsedata[i]['class'] = predicts[i]
    print('all done')
    data = pd.DataFrame.from_dict(self.parsedata)
    # print(json.dump(self.parsedata[0]))
    return data.to_json(orient='records')
    # jsons = json.dumps(self.parsedata)
    # return jsons
    # return self.load()

