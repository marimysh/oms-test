# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as et

TEMPLATE = './requests/template.xml'
OUT_DIR = './requests'


def readXml(filename):
    with open(filename, 'r') as fin:
        return et.parse(fin, et.XMLParser(encoding='utf-8'))


def writeXml(filename, xml):
    with open(filename, 'w') as fout:
        xml.write(fout, encoding='utf-8')


def substituteParameter(root, parent, mapping):
    for node in root.iter(parent):
        for key, value in mapping.iteritems():
            if node.find('Name').text == key:
                node.find('Value').text = str(value)
    return root


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("""Usage: %s cfs_spec_id instance_id""" % sys.argv[0])
        sys.exit(0)
    cfs_spec_id = sys.argv[1]
    instance_id = sys.argv[2]

    xml = readXml(TEMPLATE)

    substituteParameter(xml.getroot(), 'Attribute', {'cfs_spec_id': cfs_spec_id,
                                                     'instance_id': instance_id,
                                                     'tx_id': instance_id})

    writeXml(OUT_DIR + '/' + cfs_spec_id + '.xml', xml)




