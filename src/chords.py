import datetime
import enum
import requests
import json
from flask import g, Flask
from common.config import conf
from common.logs import get_logger

logger = get_logger(__name__)


def create_get_request(path):
    chords_uri = "http://c002.rodeo.tacc.utexas.edu:31108" + path;
    getData = {'email': conf.chords_user_email,
               'api_key': conf.chords_api_key}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.get(chords_uri, data=getData, headers=headers, verify=False)
    time = res.elapsed.total_seconds()
    logger.debug(res.content)
    print(time)
    return res

def create_post_request(path,postData):
    chords_uri = conf.chords_url + path;
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.post(chords_uri, data=postData, headers=headers,verify=False)
    logger.debug(res.content)
    return res

def list_measurements(instrument_id, start, end):
    path = "/instruments/" + instrument_id + ".json?"  # "api/v1/data.json";
    # start, end, instruments
    logger.debug(start)
    logger.debug(end)
    res = create_get_request(path);
    if (res.status_code == 200):
        message = "Measurement found"
    else:
        message='Measurements not found'
    logger.debug(message)
    logger.debug(res)
    return json.loads(res.content.decode('utf-8')), message
