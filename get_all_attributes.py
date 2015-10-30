# -*- coding: utf-8 -*-
__author__ = 'mike'
import sys
import os
from construct_responses import *
import lxml.etree
from codecs import open as uopen
import unicodecsv as csv

def parseCFS(filename):
    xml = readXml(filename)
    attributes = dict()
    for attr in xml.getroot().iter('Attribute'):
        try:
            #print attr.find('Name').text, attr.find('Value').text
            value = attr.find('Value').text
            attributes[attr.find('Name').text] = value
        except Exception as e:
            print 'error', e

    return attributes

def main():
    if len(sys.argv) < 3:
        print 'Usage: %s request_dir output' % sys.argv[0]
        sys.exit(0)

    req_dir = sys.argv[1]
    out_name = sys.argv[2]

    files = os.listdir(req_dir + '/')

    all_attributes = dict()

    for file in files:
        if file.endswith('.xml'):
            print 'Parsing', file
            cfs = file.split('.xml')[0]
            all_attributes[cfs] = parseCFS(req_dir + '/' + file)

    attributes = set()
    map(lambda cfs: attributes.update(all_attributes[cfs].keys()), all_attributes.keys())

    attributes = list(attributes)

    with open(out_name, 'w') as fout:
        print "Writing", out_name
        #csv.get_dialect('excel').delimiter = ' '
        writer = csv.DictWriter(fout, attributes, dialect='excel')

        #writer.writerow(attributes)
        writer.writeheader()
        for csf, attrs in all_attributes.iteritems():
            writer.writerow(attrs)
            #writer.writerow(row)

if __name__ == '__main__':
    main()