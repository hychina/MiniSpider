import logging
import sys

def log(name, msg):
    msg = ' [{}] {}'.format(name, msg)
    sys.stdout.write(msg+'\n')
    logging.debug(msg)

