import os
import xml.etree.ElementTree as et

REQUEST_DIR = './requests/'

for file in filter(os.path.isfile, map(lambda f: REQUEST_DIR + f, os.listdir(REQUEST_DIR))):
    try:
        et.parse(open(file, 'r'))
    except:
        print file
