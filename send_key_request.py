# -*- coding: utf-8 -*-

import sys
import random
from construct_responses import *
from send_request import sendRequest2
import io

OMS = 'http://rt-sa-app-2.ds.local:8180/lyra-adapter/LyraOmsService'
LOC = 'http://127.0.0.1:8080/'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s orderkey components" % sys.argv[0])
        sys.exit(0)
    order_key = sys.argv[1]
    random.seed(time.time())
    components = sys.argv[2:]

    for id in components:
        request_file = './requests/' + id + '.xml'
        xml = readXml(request_file)

        substituteParameter(xml.getroot(), 'Attribute', {'main_virtual_number': order_key,
                                                         'instance_id': random.randint(1, 10000000)})

        print('Sending ' + id)

        stream = io.BytesIO()
        xml.write(stream, encoding='utf-8')
        request = stream.getvalue().decode('utf-8')

        sendRequest2(request, 5)




 