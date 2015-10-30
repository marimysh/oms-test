import sys, time
import subprocess as sp

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s n_orders starting_key components...' % sys.argv[0]
        sys.exit(0)

    n_orders = int(sys.argv[1])
    start = int(sys.argv[2])
    components = ' '.join(sys.argv[3:])
    pcs = []
    for key in range(start, start + n_orders):
        pcs.append(sp.Popen('python send_key_request.py ' + str(key) + ' ' + components, shell=True))
        time.sleep(2)

    for pc in pcs:
        pc.wait()