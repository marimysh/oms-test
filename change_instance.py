import sys
import os
import xml.etree.ElementTree as et
import copy

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
                node.find('Value').text = value
    return root

def getParameter(root, parent, parameter):
    for node in root.iter(parent):
        if node.find('Name').text == parameter:
            return  node.find('Value').text

def win32_unicode_argv():
    """Uses shell32.GetCommandLineArgvW to get sys.argv as a list of Unicode
    strings.

    Versions 2.x of Python don't support Unicode in sys.argv on
    Windows, with the underlying Windows API instead replacing multi-byte
    characters with '?'.
    """

    from ctypes import POINTER, byref, cdll, c_int, windll
    from ctypes.wintypes import LPCWSTR, LPWSTR

    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)

    cmd = GetCommandLineW()
    argc = c_int(0)
    argv = CommandLineToArgvW(cmd, byref(argc))
    if argc.value > 0:
        # Remove Python executable and commands if present
        start = argc.value - len(sys.argv)
        return [argv[i] for i in
                xrange(start, argc.value)]



if __name__ == '__main__':
    sys.argv = win32_unicode_argv()
    if len(sys.argv) < 3:
        print 'Usage: %s dir value' % sys.argv[0]
        sys.exit(0)

    dir = sys.argv[1]
    parameter = 'instance_id'
    value = ' '.join(sys.argv[2:])
    #value = sys.argv[3]
    #print value, type(value)
    #sys.exit(0)
    for file in os.listdir(dir):
        try:
            filename = dir + '/' + file
            print filename
            xml = readXml(filename)
            old = copy.deepcopy(xml)
            inst_id = getParameter(xml.getroot(), 'Attribute', parameter)
            substituteParameter(xml.getroot(), 'Attribute', {parameter: value + inst_id})
            try:
                writeXml(filename, xml)
            except Exception as e:
                print 'Writing error:', e
                writeXml(old)
        except Exception as e:
            print 'Error:', e