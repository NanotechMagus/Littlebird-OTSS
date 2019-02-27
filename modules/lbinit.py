# Standard Library Imports
import logging
import configparser
from pathlib import Path

# Locally Developed Imports

# Third Party Imports


def initialize(isnew=False):
    # get absolute path for use throughout the initialization phase
    absdir = str(Path().resolve().parent)
    print(absdir)
    # Check for built configfile.json.

    # If no configfile.json, get configparse information

    # Do something if isnew flag is flipped
    if not isnew:
        try:
            print('Is not new!')
        except Exception as err:
            raise err

    return


def firstrun():
    # Build configfile in json


    return



def configload(abspath: str):
    # Use configparse to load config data into a dict
    print(f'Checking config file at {abspath}/conf/littlebird.ini')

    config = configparser.ConfigParser()
    config.read(abspath + '/conf/littlebird.ini')
    return dict(config._sections)


