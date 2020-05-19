import datetime
import enum
import requests
import json
from flask import g, Flask
from common.config import conf
from common.logs import get_logger

logger = get_logger(__name__)


def create_get_request(path):
    chords_uri = conf.chords_url + path;
    getData = {'email': conf.chords_user_email,
               'api_key': conf.chords_api_key}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.get(chords_uri, data=getData, headers=headers, verify=False)
    logger.debug(res.content)
    return res

def create_post_request(path,postData):
    chords_uri = conf.chords_url + path;
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.post(chords_uri, data=postData, headers=headers,verify=False)
    logger.debug(res.content)
    return res

def list_sites():
    #GET get a site from chords service
    res = create_get_request("/sites.json")
    if (res.status_code == 200):
        message = "Sites found"
    else:
        raise logger.debug(msg=f'No Site found')
    logger.debug(message)
    logger.debug(res)
    return json.loads(res.content.decode('utf-8')),message

