#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
import copy
import time
import requests
from codecs import open as uopen

TEMPLATE_DIR = './templates/'


def readXml(filename):
    with open(filename, 'r') as fin:
        return et.parse(fin, et.XMLParser(encoding='utf-8'))


def writeXml(filename, xml):
    with open(filename, 'w') as fout:
        xml.write(fout, encoding='utf-8')


def substituteValues(root, mapping):
    for node in root.iter():
        for key, value in mapping.iteritems():
            if node.tag == key:
                node.text = str(value)
    return root


def substituteParameter(root, parent, mapping):
    for node in root.iter(parent):
        for key, value in mapping.iteritems():
            if node.find('Name').text == key:
                node.find('Value').text = str(value)
    return root


def getParameter(root, parent, parameter):
    for node in root.iter(parent):
        if node.find('Name').text == parameter:
            return node.find('Value').text


def getTagText(root, tag):
    for node in root.iter(tag):
        return node.text


def _WFM_construct(operation, order_id, components):
    template = readXml(TEMPLATE_DIR + 'WFM_' + operation + '.xml')
    mapping = {'nz': components[0]['instance_id']}
    root = substituteValues(template.getroot(), mapping)

    service = None
    parent = None

    for node in root.iter('service'):
        service = copy.deepcopy(node)
    for node in root.iter('servicesInstallationResult'):
        parent = node

    for component in components[1:]:
        parent.append(substituteValues(service, {'nz': component['instance_id']}))
        service = copy.deepcopy(service)

    return template


def WFM_FinishVisit(order_id, components, RESPONSE_DIR):
    if len(components) < 1:
        return
    print 'WFM_FinishVisit for %s' % ' '.join(map(lambda x: x['id'], components))
    writeXml(RESPONSE_DIR + 'WFM_FinishVisitSuccess_all.xml',
             _WFM_construct('FinishVisitSuccess', order_id, components))
    writeXml(RESPONSE_DIR + 'WFM_FinishVisitFail_all.xml',
             _WFM_construct('FinishVisitFail', order_id, components))


def _HPSA_construct(operation, order_id, cfs_spec_id, instance_id):
    template = readXml(TEMPLATE_DIR + 'HPSA_' + operation + '.xml')
    mapping = {'specId': cfs_spec_id, 'instanceId': instance_id, 'orderId': order_id}
    substituteValues(template.getroot(), mapping)
    return template


def _HPSA_write(operation, order_id, components, RESPONSE_DIR):
    for component in components:
        writeXml(RESPONSE_DIR + 'HPSA_' + operation + '_' + component['id'] + '.xml',
                 _HPSA_construct(operation, order_id, component['id'], component['instance_id']))


def HPSA_Activate(order_id, components, RESPONSE_DIR):
    print 'HPSA_Activate for %s' % ' '.join(map(lambda x: x['id'], components))
    _HPSA_write('ActivateSuccess', order_id, components, RESPONSE_DIR)
    _HPSA_write('ActivateFail', order_id, components, RESPONSE_DIR)

def HPSA_Cancel(order_id, components, RESPONSE_DIR):
    print 'HPSA_Cancel for %s' % ' '.join(map(lambda x: x['id'], components))
    _HPSA_write('CancelSuccess', order_id, components, RESPONSE_DIR)


def HPSA_Commit(order_id, components, RESPONSE_DIR):
    print 'HPSA_Commit for %s' % ' '.join(map(lambda x: x['id'], components))
    _HPSA_write('CommitSuccess', order_id, components, RESPONSE_DIR)
    _HPSA_write('CommitFail', order_id, components, RESPONSE_DIR)


def HPSA_Validate(order_id, components, RESPONSE_DIR):
    print 'HPSA_Validate for %s' % ' '.join(map(lambda x: x['id'], components))
    _HPSA_write('ValidateFail', order_id, components, RESPONSE_DIR)
    _HPSA_write('ValidateSuccess', order_id, components, RESPONSE_DIR)


def _LYRA_construct(operation, order_id, instance_id):
    template = readXml(TEMPLATE_DIR + 'LYRA_' + operation + '.xml')
    substituteValues(template.getroot(), {'ComponentId': instance_id})
    substituteParameter(template.getroot(), 'Parameter', {'orderId': order_id})

    return template


def _LYRA_Cancel_construct(operation, order_id, instance_id):
    template = readXml(TEMPLATE_DIR + 'LYRA_' + operation + '.xml')
    substituteValues(template.getroot(), {'ComponentId': instance_id, 'OrderId': order_id})

    return template

def _LYRA_write(operation, order_id, components, RESPONSE_DIR, construct=_LYRA_construct):
    for component in components:
        writeXml(RESPONSE_DIR + 'LYRA_' + operation + '_' + component['id'] + '.xml',
                 construct(operation, order_id, component['instance_id']))


def LYRA_ConfirmCall(order_id, components, RESPONSE_DIR):
    print 'LYRA_ConfirmCall for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('ConfirmCallFail', order_id, components, RESPONSE_DIR)
    _LYRA_write('ConfirmCallSuccess', order_id, components, RESPONSE_DIR)

def LYRA_Cancel(order_id, components, RESPONSE_DIR):
    print 'LYRA_Cancel for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('CancelSuccess', order_id, components, RESPONSE_DIR, _LYRA_Cancel_construct)

def LYRA_ConfirmOrder(order_id, components, RESPONSE_DIR):
    print 'LYRA_ConfirmOrder for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('ConfirmOrderSuccess', order_id, components, RESPONSE_DIR)
    _LYRA_write('ConfirmOrderFail', order_id, components, RESPONSE_DIR)


def LYRA_Install(order_id, components, RESPONSE_DIR):
    print 'LYRA_Install for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('InstallFail', order_id, components, RESPONSE_DIR)
    _LYRA_write('InstallSuccess', order_id, components, RESPONSE_DIR)
	
def LYRA_RemoveFTTX(order_id, components, RESPONSE_DIR):
    print 'LYRA_RemoveFTTX for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('RemoveFTTXFail', order_id, components, RESPONSE_DIR)
    _LYRA_write('RemoveFTTXSuccess', order_id, components, RESPONSE_DIR)

def LYRA_Rc(order_id, components, RESPONSE_DIR):
    print 'LYRA_Rc for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('RcSuccess', order_id, components, RESPONSE_DIR)
    _LYRA_write('RcFail', order_id, components, RESPONSE_DIR)

def LYRA_ServiceDesk(order_id, components, RESPONSE_DIR):
    print 'LYRA_ServiceDesk for %s' % ' '.join(map(lambda x: x['id'], components))
    _LYRA_write('ServiceDeskSuccess', order_id, components, RESPONSE_DIR)
    _LYRA_write('ServiceDeskFail', order_id, components, RESPONSE_DIR)