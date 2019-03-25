# Standard Library Imports
import logging
import json
import sys
import os

# Locally Developed Imports

# Third Party Imports


class lbInit:

    def __init__(self):
        self.isnew = False
        self.basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.confpath = os.path.join(self.basedir, 'conf')
        self.config = self.configload()

    def firstrun(self, abspath):
        # Build configfile in json

        return

    def configload(self):
        # Use configparse to load config data into a dict
        # logging.info(f'Checking config file at {self.confpath}/littlebird.ini')

        if os.path.exists(os.path.join(self.confpath, "lbconfmaster.json")):
            try:
                with open(os.path.join(self.confpath, 'lbconfmaster.json'), 'r') as f:
                    config = json.load(f)
                return config
            except Exception as err:
                print(f'Error loading configuration file at '
                      f'{os.path.join(self.confpath, "lbconfmaster.json")}.\nError: {err}')
                raise
        elif os.path.exists(os.path.join(self.confpath, "lbconf.json")):
            try:
                with open(os.path.join(self.confpath, 'lbconf.json'), 'r') as f:
                    config = json.load(f)
                return config
            except Exception as err:
                print(f'Error loading configuration file at '
                      f'{os.path.join(self.confpath, "lbconf.json")}.\nError: {err}')
                raise
        else:
            print(f'No configuration file present!\n Looking for config at '
                  f'{os.path.join(self.confpath, "lbconf.json")}')
            return None

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
