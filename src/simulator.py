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


# Create measurements using the Streams API
def create_measurements_streams():
    log_file = 'timelog.txt'
    total_time = 0.0
    myfile = open('timelog.txt', 'a')
    for i in range(0, 5):
        datetime_now = datetime.now().isoformat()
        start = time.time()
        temp = randint(85, 100)
        result = t.streams.create_measurement(inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              vars=[{"var_id": "temp", "value": temp },
                                                    {"var_id": "spc", "value": randint(240, 300)},
                                                    {"var_id": "turb", "value": randint(10, 19)},
                                                    {"var_id": "ph", "value": randint(1, 10)},
                                                    {"var_id": "batv", "value": round(random.uniform(10, 13), 2)}],
                                              datetime=datetime_now, _tapis_debug=True)

        #time.sleep(60.0)
        #elapsed = time.time() - start
        #total_time = round(elapsed, 2) + total_time
       # myfile.write(str(i) + ":" + str(round(elapsed, 2)) + "\n")
        #print("Measurement creation")
        print(temp)
    #print(total_time/5.0)
    #myfile.close()


# Download measurements with Streams API
def download_measurements_streams():
    log_file = 'timelog.txt'
    total_time = 0.0
    myfile = open('timelog.txt', 'a')
    for i in range(0, 500):
        datetime_now = datetime.now().isoformat()
        start = time.time()
        ## We can include a start_date and end_date in this call to list measurements
        result = t.streams.list_measurements(inst_id='Ohio_River_Robert_C_Byrd_Locks',project_uuid='wq_demo_project', site_id='wq_demo_site',
                                             start_date='2020-05-18T22:16:25Z',end_date='2020-05-21T22:16:25Z',format='csv',_tapis_debug=True)
        elapsed = time.time() - start
        total_time = round(elapsed, 2) + total_time
        myfile.write(str(i) + ":" + str(round(elapsed, 2)) + "\n")
        print("Measurements fetch")
       # print(result)
    print(total_time/500.0)
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
    print("site creation")
    print(result)

    ## Create Instruments
    result, debug = t.streams.create_instrument(project_uuid='wq_demo_project',topic_category_id ='2',site_id='wq_demo_site',
                                                inst_name='Ohio_River_Robert_C_Byrd_Locks',inst_description='demo instrument',
                                                inst_id='Ohio_River_Robert_C_Byrd_Locks', _tapis_debug=True)
    print("Instrument creation")
    print(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project',topic_category_id ='2',
                                              site_id='wq_demo_site',inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='temperature', shortname='temp',var_id='temp', _tapis_debug=True)
    print("Temperature Variable creation")
    print(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='battery', shortname='bat', var_id='batv',
                                              _tapis_debug=True)
    print("Battery Variable creation")
    print(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='specific_conductivity', shortname='spc', var_id='spc',
                                              _tapis_debug=True)
    print("Specific conductivity Variable creation")
    print(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='turbidity', shortname='turb', var_id='turb',
                                              _tapis_debug=True)
    print("Turbidity Variable creation")
    print(result)

    ## Create Variables
    result, debug = t.streams.create_variable(project_uuid='wq_demo_project', topic_category_id='2',
                                              site_id='wq_demo_site', inst_id='Ohio_River_Robert_C_Byrd_Locks',
                                              var_name='ph_level', shortname='ph', var_id='ph',
                                              _tapis_debug=True)
    print("Ph Variable creation")
    print(result)

## Create templates and channels
def create_template():
    '''
    result,debug = t.streams.create_template(template_id='demo_wq_data_test_template10', type='stream', script='var periodCount=1\n '
                    'var every=0s\n var crit lambda \n var channel_id string\n stream\n    |from()\n        .measurement(\'tsdata\')\n        '
                    ' .groupBy(\'var\')\n     |window()\n        .period(period)\n         .every(every)\n         .align()\n     |alert()\n       '
                    ' .id(channel_id +  \' {{ .Name }}/{{ .Group }}/{{.TaskName}}/{{index .Tags \"var\" }}\')\n         .crit(crit)\n       '
                    '  .message(\'{{.ID}} is {{ .Level}} at time: {{.Time}} as value: {{ index .Fields \"value\" }} exceeded the threshold\')\n       '
                    ' .details(\'\')\n         .post()\n         .endpoint(\'api-alert\')\n     .captureResponse()\n    |httpOut(\'msg\')', _tapis_debug=True)
    '''
    result, debug = t.streams.create_template(template_id='demo_wq_data_test_template12', type='stream',
                                              script=' var crit lambda \n var channel_id string\n stream\n    |from()\n        .measurement(\'tsdata\')\n        '
                                                     ' .groupBy(\'var\')\n   |alert()\n       '
                                                     ' .id(channel_id +  \' {{ .Name }}/{{ .Group }}/{{.TaskName}}/{{index .Tags \"var\" }}\')\n         .crit(crit)\n    .noRecoveries()\n      '
                                                     '  .message(\'{{.ID}} is {{ .Level}} at time: {{.Time}} as value: {{ index .Fields \"value\" }} exceeded the threshold\')\n       '
                                                     ' .details(\'\')\n         .post()\n         .endpoint(\'api-alert\')\n     .captureResponse()\n    |httpOut(\'msg\')', _tapis_debug=True)
    # Actor id=7kxayXzzX63oY, nonce= TACC-PROD_Xr3LW5MOZXGkv, maxUses =100

def create_channel():
    result,debug =  t.streams.create_channels(channel_id='demo_wq_test_32', channel_name='demo.wq.test', template_id='demo_wq_data_test_template12',
                                              triggers_with_actions=[{"inst_ids":["Ohio_River_Robert_C_Byrd_Locks"],"condition":{"key":"Ohio_River_Robert_C_Byrd_Locks.temp","operator":">", "val":90}, "action":{"method":"ACTOR","actor_id" :"4VQZ540z1P3Gm","message":"Instrument: Ohio_River_Robert_C_Byrd_Locks temp exceeded threshold", "abaco_base_url":"https://api.tacc.utexas.edu","nonces":"TACC-PROD_7KZppEa8Vrrm3"}}]
                                              ,_tapis_debug=True)

if __name__ == "__main__":
    t = DynaTapy(base_url='https://dev.develop.tapis.io', username='testuser6', account_type='user', password='testuser6', tenant_id='dev')
    t.get_tokens()
    #create_project_site_inst_var()
    #create_template()
    #create_channel()
    create_measurements_streams()
    #download_measurements_streams()
    #download_measurements_chords(9)

