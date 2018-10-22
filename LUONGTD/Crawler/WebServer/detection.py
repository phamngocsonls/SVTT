from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging 
import re
import json

def error_to_str(e):
    return str(e).replace('\n', '\\n')    

def read_clues():
    filename = os.path.join(os.path.dirname(__file__), 'etc/apps2.json')

    logging.info("Reading clues file %s", filename)
    try:
        json_data = open(filename)
    except IOError as e:
        logging.error("Error while opening clues file, terminating: %s", error_to_str(e))
        raise

    try:
        clues = json.load(json_data, encoding='utf-8')
    except ValueError as e:
        logging.error("Error while reading JSON file, terminating: %s", error_to_str(e))
        raise

    json_data.close()
    apps = clues['apps']
    return apps

def check_header(wsv, apps):
    wsv = wsv.lower()
    for app in apps:
        for entry in apps[app]["headers"]:
            if entry == "Server" or entry == "X-Powered-By" or entry == "Set-Cookie":                
                if re.search(apps[app]["headers"][entry].lower(), wsv):
                    return app
    return wsv
