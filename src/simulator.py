import requests
from tapy.dyna import DynaTapy
import json
import os
import timeit
from datetime import datetime
from common.config import conf
from random import randint
import random
import time

# get the logger instance -
from common.logs import get_logger
logger = get_logger(__name__)




def download_measurements_chords(instrument_id, start="", end="", format="json"):
    myfile = open('timelog.txt', 'a')
    path = "/instruments/" + str(instrument_id) +'.csv'
  # "api/v1/data.json";
    chords_uri = "http://c002.rodeo.tacc.utexas.edu:31108" + path;
    getData = {'email': 'admin@chordsrt.com',
               'api_key': 'LPYSixTTM3BRcreZE2pP'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = requests.get(chords_uri, data=getData, headers=headers, verify=False)
    time = res.elapsed.total_seconds()
    print(time)
    if (res.status_code == 200):
        message = "Measurement found"
    else:
        message='Measurements not found'
    logger.debug(message)
    logger.debug(res)
    return (res.content.decode('utf-8'))


def create_measurements_streams():
    log_file = 'timelog.txt'
    total_time = 0.0
    myfile = open('timelog.txt', 'a')
    for i in range(0, 1000):
        datetime_now = datetime.now().isoformat()
        start = time.time()
        result = t.streams.create_measurement(inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              vars=[{"var_id": "temp", "value": randint(10, 100)},
                                                    {"var_id": "spc", "value": randint(240, 300)},
                                                    {"var_id": "turb", "value": randint(10, 19)},
                                                    {"var_id": "ph", "value": randint(1, 10)},
                                                    {"var_id": "batv", "value": round(random.uniform(10, 13), 2)}],
                                              datetime=datetime_now, _tapis_debug=True)
        elapsed = time.time() - start
        total_time = round(elapsed, 2) + total_time
        myfile.write(str(i) + ":" + str(round(elapsed, 2)) + "\n")
        logger.debug("Measurement creation")
        logger.debug(result)
    print(total_time/1000.0)
    myfile.close()


def download_measurements_streams():
    log_file = 'timelog.txt'
    total_time = 0.0
    myfile = open('timelog.txt', 'a')
    for i in range(0, 100):
        datetime_now = datetime.now().isoformat()
        start = time.time()
        ## We can include a start_date and end_date in this call to list measurements
        result = t.streams.list_measurements(inst_id='Ohio_River_Robert_C_Byrd_Locks',project_uuid='wq_demo_project', site_id='wq_demo_site',
                                             start_date='2020-05-18T22:16:25Z',end_date='2020-05-21T22:16:25Z',format='csv',_tapis_debug=True)
        elapsed = time.time() - start
        total_time = round(elapsed, 2) + total_time
        myfile.write(str(i) + ":" + str(round(elapsed, 2)) + "\n")
        logger.debug("Measurements fetch")
        logger.debug(result)
    print(total_time/100.0)
    myfile.close()


def create_project_site_inst_var():
    ## Create Project
    result, debug = t.streams.create_project(project_name='wq_demo_project',description='project for early adopters demo',
                                             owner='testuser6', pi='ajamthe', funding_resource='tapis', project_url='test.tacc.utexas.edu',
                                             active=True,_tapis_debug=True)
    #logger.debug("project creation")
    #logger.debug(result)

    ## Create Site
    result, debug = t.streams.create_site(project_uuid='wq_demo_project',site_name='wq_demo_site', site_id='wq_demo_site',
                                          latitude=50, longitude = 10, elevation=2,description='test_site', _tapis_debug=True)
    logger.debug("site creation")
    logger.debug(result)

    ## Create Instruments
    result, debug = t.streams.create_instrument(project_uuid='wq_demo_project',topic_category_id ='2',site_id='wq_demo_site',
                                                inst_name='Ohio_River_Robert_C_Byrd_Locks',inst_description='demo instrument',
                                                inst_id='Ohio_River_Robert_C_Byrd_Locks', _tapis_debug=True)
    logger.debug("Instrument creation")
    logger.debug(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project',topic_category_id ='2',
                                              site_id='wq_demo_site',inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='temperature', shortname='temp',var_id='temp', _tapis_debug=True)
    logger.debug("Temperature Variable creation")
    logger.debug(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='battery', shortname='bat', var_id='batv',
                                              _tapis_debug=True)
    logger.debug("Battery Variable creation")
    logger.debug(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='specific_conductivity', shortname='spc', var_id='spc',
                                              _tapis_debug=True)
    logger.debug("Specific conductivity Variable creation")
    logger.debug(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='turbidity', shortname='turb', var_id='turb',
                                              _tapis_debug=True)
    logger.debug("Turbidity Variable creation")
    logger.debug(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='ph_level', shortname='ph', var_id='ph',
                                              _tapis_debug=True)
    logger.debug("Ph Variable creation")
    logger.debug(result)

## Enter the username and password for test accounts on dev
if __name__ == "__main__":
    t = DynaTapy(base_url='https://dev.develop.tapis.io', username='testuser6', account_type='user', password='testuser6', tenant_id='dev')
    t.get_tokens()
    #create_project_site_inst_var()
    #create_measurements_streams()
    download_measurements_streams()
    #download_measurements_chords(9)

