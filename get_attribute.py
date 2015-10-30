import sys, os
from construct_responses import readXml, getParameter

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s (?)attribute components(none = all)' % ()
        sys.exit(0)

    attribute = sys.argv[1]
    invert = False
    if attribute.startswith('?'):
        attribute = attribute[1:]
        invert = True
    components = sys.argv[2:]
    if len(components) == 0:
        components = map(lambda file: file.split('.')[0], os.listdir('./requests'))
    print 'Getting attribute %s' % attribute
    attributes = {}
    for component in components:
        try:
            xml = readXml('./requests/' + component + '.xml')
            attributes[component] = getParameter(xml.getroot(), 'Attribute', attribute)
        except:
            print 'ERROR parsing', component

    if invert:
        for val in sorted(set(attributes.values())):
            print val, ':', ', '.join(filter(lambda x: attributes[x] == val, attributes.keys()))
    else:
        for key, val in attributes.iteritems():
            print key, ':', val