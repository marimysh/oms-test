#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, collections
from construct_responses import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage %s order_id components...' % sys.argv[0]
        sys.exit(0)
    # cfs_ids = ['line_provision', 'internet_access']
    order_id = sys.argv[1]
    cfs_ids = sys.argv[2:]

    print 'Generating responses for order_id %s for comonents %s' % (order_id, ' '.join(cfs_ids))

    REQUEST_DIR = './requests/'
    RESPONSE_DIR = './responses/' + str(order_id) + '/'
    if not os.path.isdir('./responses/'):
        os.mkdir('./responses/')
    components = []

    for id in cfs_ids:
        xml = readXml(REQUEST_DIR + id + '.xml')
        instance_id = getParameter(xml, 'Attribute', 'instance_id')
        if instance_id is None:
            raise Exception('No component_instance_id attribute in %s' % id)
        action = getParameter(xml, 'Attribute', 'action_code')
        install = getParameter(xml, 'Attribute', 'need_installation')
        cfs = getParameter(xml, 'Attribute', 'cfs_spec_id')
        components.append({'instance_id': instance_id, 'id': id, 'action': action, 'install': install, 'cfs': cfs})

    if len(filter(lambda count: count > 1,
                  collections.Counter(map(lambda comp: comp['instance_id'], components)).values())):
        print 'Not unique instance_ids'
        #sys.exit(0)
    try:
        os.mkdir(RESPONSE_DIR)
    except:
        print 'Dir already exists, overwriting'

    #print components
    pr = lambda comp: comp['action'] in ['1', '3', '33', '54', '19', '29', '45', '1003']
    ce = lambda comp: comp['action'] in ['2', '34']
    ch = lambda comp: comp['action'] in ['7']
    raz = lambda comp: comp['action'] in ['29', '1003']
    need_inst = lambda comp: comp['install'] == '1'
    need_activation = lambda comp: comp['cfs'] not in ['equipment' , 'additional_work_installation' , 'subscriber_rental']

    call_ftr = lambda comp: pr(comp) and need_inst(comp) and not raz(comp)
    wf_ftr = call_ftr
    install_ftr = lambda comp: need_inst(comp) and (ce(comp) or raz(comp))
    activate_ftr = lambda comp: (ch(comp) or ce(comp) or pr(comp)) and need_activation(comp) and not raz(comp)
    validate_ftr = activate_ftr
    commit_ftr = validate_ftr
    hpsa_cancel_ftr = validate_ftr
    rc_ftr = activate_ftr
    confirm_ftr = lambda comp: True
    service_desk_ftr = lambda comp: True
    #commit_ftr = validate_ftr = install_ftr = call_ftr = wf_ftr = confirm_ftr
    #for id, component in components.iteritems():

    HPSA_Activate(order_id, filter(activate_ftr, components), RESPONSE_DIR)

    HPSA_Validate(order_id, filter(validate_ftr, components), RESPONSE_DIR)

    HPSA_Cancel(order_id, filter(hpsa_cancel_ftr, components), RESPONSE_DIR)

    HPSA_Commit(order_id, filter(commit_ftr, components), RESPONSE_DIR)

    LYRA_Cancel(order_id, components, RESPONSE_DIR)

    LYRA_ConfirmCall(order_id, filter(call_ftr, components), RESPONSE_DIR)

    LYRA_ConfirmOrder(order_id, filter(confirm_ftr, components), RESPONSE_DIR)

    LYRA_Install(order_id, filter(install_ftr, components), RESPONSE_DIR)

    LYRA_Rc(order_id, filter(rc_ftr, components), RESPONSE_DIR)

    LYRA_ServiceDesk(order_id, filter(service_desk_ftr, components), RESPONSE_DIR)
	
    LYRA_RemoveFTTX(order_id, filter(install_ftr, components), RESPONSE_DIR)

    WFM_FinishVisit(order_id, filter(wf_ftr, components), RESPONSE_DIR)