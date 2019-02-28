# Standard Library Imports
import logging
import configparser
from pathlib import Path
import sys

# Locally Developed Imports

# Third Party Imports


def initialize():
    # Check for built configfile.json.
    isnew = False
    # If no configfile.json, get configparse information

    # Do something if isnew flag is flipped
    if not isnew:
        try:
            print('Is not new!')
        except Exception as err:
            raise err

    return


def firstrun(abspath):
    # Build configfile in json


    return


def configload(abspath: str):
    # Use configparse to load config data into a dict
    logging.info(f'Checking config file at {abspath}/conf/littlebird.ini')

    config = configparser.ConfigParser()
    config.read(abspath + '/conf/littlebird.ini')
    logging.debug(f'Read and loaded config from {abspath}/conf/littlebird.ini')

    return dict(config._sections)


def logwrapper(init=''):
    # TODO: Differentiate between initial verbosity and configfile handler creation -- check for dict vs int
    # Check for initial verbosity
    initlevels = {0:"logging.WARN",1:"logging.INFO",2:"logging.DEBUG"}
    if not init:
        logging.basicConfig(level=logging.WARN, format='%(asctime)s %(levelname)s %(message)%',
                            datefmt="%Y-%m-%d %H:%M:%S")
        logging.info(f'Initial logging level set to '
                     f'{logging.getLevelName(logging.getLogger().getEffectiveLevel())}')
    elif type(init) == int:
        pass
    return


def cleanexit(level):
    # Attempt to exit program cleanly by closing connections

    logging.shutdown()
    sys.exit(level)
