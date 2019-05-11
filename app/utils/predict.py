
import sys
import os
import json
import pandas
import numpy
import optparse
from keras.models import Sequential, load_model
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from collections import OrderedDict
import pickle
from keras import backend as K

from urllib.parse import urlparse, parse_qs

class Prediction(object):
  def __init__(self):
    self.name = 'prediction'
    self.here = os.path.dirname(os.path.abspath(__file__))

  def predict(self, log_entry):
    for index, element in enumerate(log_entry):
      item = element
      X = {}
      parse = urlparse(item['url'])
      X['Method'] = item['method']
      X['Status'] = item['status']
      X['Path'] = str(parse.path)
      X['Query'] = str(parse.query) if parse.query else str({})
      log_entry[index] = json.dumps(X, separators=(',', ':'))    

    with open(os.path.join(self.here, 'tokenizer.pickle'), 'rb') as handle:
      ptokenizer = pickle.load(handle)

    seq = ptokenizer.texts_to_sequences(log_entry)
    max_log_length = 1024
    log_entry_processed = sequence.pad_sequences(seq, maxlen=max_log_length)
    
    model = load_model(os.path.join(self.here, 'rnn-model.h5'))
    model.load_weights(os.path.join(self.here, 'rnn-weights.h5'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    prediction = model.predict_classes(log_entry_processed)
    K.clear_session()
    return prediction