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


def logwrapper(init=False, configdata: dict = False):

    # Check for initial verbosity
    initlevels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}

    # TODO: Rebuild logwrapper to utilize configparser for logging.config.fileConfig(fname)
    # Create initial logging procedure
    logger = logging.getLogger('Littlebird')
    logger.setLevel(initlevels[init])

    # This /should/ proc only during the program boot sequence
    if not configdata:
        try:
            verbosity = logging.StreamHandler(stream=sys.stdout)
            verbosity.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)%',
                                                     datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(verbosity)
        except Exception as err:
            logging.warning(f'Error setting verbosity handler with type: {err.args}: {err}')
            cleanexit(err.args)
        finally:
            return

    # This /should/ only proc when the wrapper is called during the initialization only if configdata isn't Enabled
    elif not configdata['ENABLED']:
        try:
            verbosity = logging.StreamHandler(stream=sys.stdout)
            verbosity.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)%',
                                                     datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(verbosity)
        except Exception as err:
            logging.warning(f'Error setting verbosity handler with type: {err.args}: {err}')
        finally:
            return
    else:
        try:
            # Remove previous handler which /should/ be active
            logger.handlers.pop()

            # Create new handler for the rest of the session
            littlebird = logging.FileHandler(filename=configdata['LOCATION'] + "/" + configdata['FILENAME'],
                                             encoding='utf-8', mode='w')
            littlebird.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)%',
                                                      datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(littlebird)

        except Exception as err:
            logging.warning(f'Error setting verbosity handler with type: {err.args}: {err}')

    return


def cleanexit(level):
    # Attempt to exit program cleanly by closing connections

    logging.shutdown()
    sys.exit(level)
