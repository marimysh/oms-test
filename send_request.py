import os
import sys
import io
import time
import requests
from codecs import open as uopen
from construct_responses import *
from collections import Counter

OMS = 'http://192.168.100.91:8180/lyra-adapter/LyraOmsService'
#OMS = 'http://rt-om-app-1.ds.local:8180/lyra-adapter/LyraOmsService'
#OMS = 'http://rt-sa-app-2.ds.local:8180/lyra-adapter/LyraOmsService'
#OMS = 'http://10.185.225.34:8180/lyra-adapter/LyraOmsService'


def sendRequest2(request, timeout=None):
    try:
        # print request
        start = time.time()
        resp = requests.post(OMS, request.encode('utf-8'), headers={"Content-Type": "charset=UTF-8"},
                             timeout=timeout)
        dur = time.time() - start
        print resp.text
        xml = et.fromstring(resp.text.encode('utf-8'))
        order = getTagText(xml, 'OrderId')
        status = getTagText(xml, 'Status')
        code = getTagText(xml, 'Code')
        message = getTagText(xml, 'Description')
        print 'Returned order: %s, status: %s, code: %s, message: %s,' % (order, status, code, message),
        print 'Time: ' + str(dur)
        return order
    except Exception as e:
        print e
        #raise


def sendRequest(filename, timeout=None):
    with uopen(filename, encoding='utf-8') as fin:
        try:
            request = fin.read()
            # print request
            start = time.time()
            resp = requests.post(OMS, request.encode('utf-8'), headers={"Content-Type": "charset=UTF-8"},
                                 timeout=timeout)
            dur = time.time() - start
            # print resp.text
            xml = et.fromstring(resp.text)
            status = getTagText(xml, 'Status')
            code = getTagText(xml, 'Code')
            message = getTagText(xml, 'Description')
            print status, code, message
            print 'Time: ' + str(dur)
        except Exception as e:
            print e


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print """Usage: %s order_key components""" % sys.argv[0]
        sys.exit(0)
    order_key = sys.argv[1]
    components = sys.argv[2:]

    inst_ids = []
    for id in components:
        inst_ids.append(getParameter(readXml('./requests/' + id + '.xml').getroot(), 'Attribute', 'instance_id'))

    if len(filter(lambda x: x > 1, Counter(inst_ids).values())) > 0:
        print 'Instance Ids not unique'
        sys.exit(0)

    orderId = None
    for id in components:
        request_file = './requests/' + id + '.xml'
        xml = readXml(request_file)
        try:
            substituteParameter(xml.getroot(), 'Attribute', {'main_virtual_number': int(order_key)})
        except:
            pass

        print('Sending ' + id)

        stream = io.BytesIO()
        xml.write(stream, encoding='utf-8')
        request = stream.getvalue().decode('utf-8')

        order = sendRequest2(request, 21)
        if orderId is None:
            orderId = order
        if order != orderId:
            print 'WARNING different orderIds in this batch'

    # order = raw_input('Input order_id ')
    print '_' * 50 + '\n'
    try:
        order = str(int(orderId))
        os.system('python generate_responses.py %s %s' % (order, ' '.join(components)))
    except:
        print """Not valid order_id, exiting.
You can manually generate responses with
generate_responses.py $order_id$ %s""" % ' '.join(components)