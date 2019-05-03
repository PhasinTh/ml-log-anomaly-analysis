import time
import pandas as pd
from .logparser import LogParser as logparser

class MLProcess(object):
  def __init__(self, file):
    start = time.time()
    self.logs = self.loadata(file)
    self.parse()
    print('take time {} ms'.format((time.time() - start)))


  def build_pattern(self, format=None):
    common_format = '<remote_addr> <identd> <remote_user> \[<date_time>\] \"<method> <path> <version>\" <status> <bytes> \"<referer>\" \"<user_agent>\"'
    if format is not None:
      return logparser(format).get_pattern()
    return logparser(common_format).get_pattern()

  def parse(self):
    for line in enumerate(self.logs.split('\r\n')):
      line = str(line).strip()
      if line:
        
        

  def loadata(self, stream, buffer_size=16384):
    data = bytearray()
    while 1:
      buff = stream.read(buffer_size)
      if not buff:
        break
      data.extend(buff)
    logs = data.decode('utf-8')
    return logs
  
