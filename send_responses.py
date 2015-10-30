import os, sys
import requests
from codecs import open as uopen
import xml.etree.ElementTree as et
from construct_responses import *
import io

#HOST = 'http://rt-om-app-1.ds.local:8180'
HOST = 'http://192.168.100.91:8180'
#HOST = 'http://rt-sa-app-2.ds.local:8180'
LYRA = HOST + '/lyra-adapter/LyraOmsService'
HPSA = HOST + '/hpsa-adapter/ActivatorCallbackService'
WFM = HOST + '/wfm-adapter/WfmToLiraApiService'
#LYRA = 'http://localhost:5553/'

def HPSAResp(text):
    xml = et.fromstring(text)
    code = getTagText(xml, 'resultCode')
    message = getTagText(xml, 'resultText')
    return 'code %s, message %s' % (code, message)


def LYRAResp(text):
    xml = et.fromstring(text)
    code = getTagText(xml, 'Code')
    message = getTagText(xml, 'Description')
    return 'code %s, message %s' % (code, message)


def WFMResp(text):
    xml = et.fromstring(text)
    code = getTagText(xml, 'errorCode')
    message = getTagText(xml, 'errorMsg')
    return 'code %s, message %s' % (code, message)


def defaultResp(text):
    return text


address = {'LYRA': LYRA, 'WFM': WFM, 'HPSA': HPSA}

systems = {'L': {'name': 'LYRA', 'resp': LYRAResp,
                 'methods': {'C': 'ConfirmCall', 'O': 'ConfirmOrder', 'I': 'Install', 'R': 'Rc', 'S': 'ServiceDesk', '_': 'Cancel', 'F': 'RemoveFTTX'}},
           'W': {'name': 'WFM', 'resp': WFMResp, 'methods': {'F': 'FinishVisit'}},
           'H': {'name': 'HPSA', 'resp': HPSAResp, 'methods': {'A': 'Activate', 'V': 'Validate', 'C': 'Commit', '_': 'Cancel'}}}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print """Usage: %s orderId system[W|L|H]method component[#|all]""" % sys.argv[0]
        sys.exit(0)
    try:
        system, method, result = tuple(sys.argv[2])
    except:
        print 'Invalid argument %s' % sys.argv[2]
        sys.exit(0)

    service_desk = system == 'L' and method == 'S'
    try:
        method = systems[system]['methods'][method]
        system = systems[system]['name']
        result = {'S': 'Success', 'F': 'Fail'}[result]
    except:
        print 'Unknown system, method or result'
        sys.exit(0)

    order_id = sys.argv[1]
    component = 'all'
    if len(sys.argv) > 3:
        component = sys.argv[3]

    task_name = None
    if service_desk:
        try:
            task_name = sys.argv[4]
        except:
            print 'Forgot task_name'
            sys.exit(0)


    # print order_id, system, method, component
    responses = os.listdir('./responses/' + order_id)
    #print responses
    valid = []
    for file in responses:
        if file.startswith(system + '_' + method + result):
            valid.append(file)

    #print valid
    existing_components = map(lambda file: '_'.join(file.split('.')[0].split('_')[2:]), valid)
    #print existing_components
    if component == 'all':
        component = existing_components
    elif component in existing_components or system:
        component = [component]
    else:
        print 'No request found for component %s' % component
        sys.exit(0)

    timeout = 0.5 if method == 'ConfirmOrder' else 2

    for id in component:
        file_name = './responses/' + order_id + '/' + system + '_' + method + result + '_' + id + '.xml'
        print 'Sending %s %s %s %s' % (system, method, result, id)
        try:

            xml = readXml(file_name)
            if service_desk:
                substituteParameter(xml.getroot(), 'Parameter', {'task_name': task_name})

            stream = io.BytesIO()
            xml.write(stream, encoding='utf-8')
            req = stream.getvalue().decode('utf-8')

            resp = requests.post(address[system], req.encode('utf-8'),
                                     headers={"Content-Type": "charset=UTF-8"}, timeout=timeout)
            print systems[system[0]]['resp'](resp.text.encode('utf-8'))
        except Exception as e:
            if method != 'ConfirmOrder':
                print e