import logging
import sys

def log(name, msg):
    msg = ' [%s] %s' % (name, msg)
    sys.stdout.write(msg+'\n')
    logging.debug(msg)

