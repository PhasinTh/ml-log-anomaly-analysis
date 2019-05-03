#!/usr/bin/env python3
# File name: logparser.py
# =============================================================================
# Author: Phasin Thosaeng
# Date created: 02/11/2019
# Date last modified: 02/26/2019
# =============================================================================

import re
import pandas as pd
import os
import time

class LogParser():
    def __init__(self, log_format, in_dir = '', out_dir = ''):
        self.path = in_dir
        self.log_format = log_format
        self.savepath = out_dir
        self.support = ['csv', 'json']  # Support Extensions
    
    def get_pattern(self):
        header, regex = self.generate_regex(self.log_format)
        return regex

    def generate_regex(self, logformat):
        '''
        function for generate regular expression
        '''
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(r'^\s+',' +', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex
    
    def parse(self, filename, filetype='csv'):
        start_time = time.time()
        filepath = os.path.join(self.path, filename)
        self.filename = filename
        headers, regex = self.generate_regex(self.log_format)
        self.df_log = self.log_to_dataframe(filepath, regex, headers, self.log_format)
        newfile = self.write_to_file(filetype)
        print('Parsing Complete!! [Time taken: {0:.6f} ms]'.format(time.time() - start_time))
        return newfile

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        log_messages = []
        linecount = 0
        with open(log_file, 'r') as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        log_df = pd.DataFrame(log_messages, columns=headers)
        return log_df
      
    def write_to_file(self, filetype):
        if(filetype in self.support):
            filename = os.path.join(self.savepath, self.filename + '.' + filetype)
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    raise
            if os.path.exists(filename):
               filename = os.path.join(self.savepath, self.filename + '_' + str(int(time.time())) + '.' + filetype)

            f = open(filename, 'w+')
            try:
                if(filetype == 'csv'):
                    newfile = f.write(self.df_log.to_csv(index=False))
                elif(filetype == 'json'):
                    newfile = f.write(self.df_log.to_json(orient='records'))
                print("Result file was written to {}".format(filename))
            except IOError as err:
                raise
        else:
            print ("ERROR !! Could not write file : \"{}\"".format(filetype))
            raise SystemExit
