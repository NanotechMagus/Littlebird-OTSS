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
    print(f'Checking config file at {abspath}/conf/littlebird.ini')

    config = configparser.ConfigParser()
    config.read(abspath + '/conf/littlebird.ini')
    return dict(config._sections)


def logwrapper(level):

    try:
        if not level:
            logging.basicConfig(level=logging.WARN)
            logging.info('Logging information ')
    except Exception as err:
        raise err

    return


def cleanexit(level):
    # Attempt to exit program cleanly by closing connections

    sys.exit(level)
