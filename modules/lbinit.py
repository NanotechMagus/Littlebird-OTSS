# Standard Library Imports
import logging
import json
import sys
import os

# Locally Developed Imports

# Third Party Imports


class lbInit:

    def __init__(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        self.isnew = False
        self.basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.confpath = os.path.join(self.basedir, 'conf')
        self.config = self.configload()
        # self.logwrapper()

    def configload(self):
        # Use configparse to load config data into a dict
        logging.info(f'Checking config file at {self.confpath}littlebird.ini')

        if os.path.exists(os.path.join(self.confpath, "lbconfmaster.json")):
            try:
                with open(os.path.join(self.confpath, 'lbconfmaster.json'), 'r') as f:
                    config = json.load(f)
                logging.info(f'Config file found!  Reading {os.path.join(self.confpath, "lbconfmaster.json")}.')
                return config
            except Exception as err:
                logging.warning(f'Error loading configuration file at '
                      f'{os.path.join(self.confpath, "lbconfmaster.json")}.\nError: {err}')
                raise
        elif os.path.exists(os.path.join(self.confpath, "lbconf.json")):
            try:
                with open(os.path.join(self.confpath, 'lbconf.json'), 'r') as f:
                    config = json.load(f)
                logging.info(f'Config file found!  Reading {os.path.join(self.confpath, "lbconf.json")}.')
                return config
            except Exception as err:
                logging.warning(f'Error loading configuration file at '
                      f'{os.path.join(self.confpath, "lbconf.json")}.\nError: {err}')
                raise
        else:
            logging.warning(f'No configuration file present!\n Looking for config at '
                  f'{os.path.join(self.confpath, "lbconf.json")}')
            return None

    def initlog(self):

        try:
            print('Starting logger.')
            logger = logging.getLogger('Littlebird')
            logger.setLevel(logging.DEBUG)

            verbosity = logging.StreamHandler()
            verbosity.setLevel(logging.DEBUG)
            verbosity.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                                     , datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(verbosity)
            logging.info('Initial Logging Stream started.')
            print('Initial Logging Stream started.')
        except Exception as err:
            print(f'Error setting verbosity handler with type: {err.args}: {err}')

        finally:
            return

    def logwrapper(self):

        # Check for initial verbosity
        initlevels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}

        # Create initial logging procedure
        logger = logging.getLogger('Littlebird')
        logger.setLevel(logging.DEBUG)

        # This /should/ proc only during the program boot sequence

        # This /should/ only proc when the wrapper is called during the initialization only if configdata isn't Enabled

        try:
            logging.info('Removing previous handler which should be active.')
            try:
                logger.removeHandler('verbosity')
            except Exception as err:
                logging.warning(f'No initial handler to remove! {err}')

            if self.config["Discord-Logging"]["ENABLED"]:
                loggerpath = os.path.join(self.basedir, self.config['Discord-Logging']['LOCATION'],
                                          self.config['Discord-Logging']['FILENAME'])
                if self.setLogdir(loggerpath):
                    # Create new handler for the rest of the session
                    littlebird = logging.FileHandler(filename=loggerpath, encoding='utf-8', mode='w')
                else:
                    littlebird = logging.StreamHandler()
            elif not self.config["Discord-Logging"]["ENABLED"]:
                littlebird = logging.StreamHandler()
            else:
                print(f'Error setting logging Handler.')

            littlebird.setLevel(initlevels[self.config["Discord-Logging"]["DEFAULTLEVEL"]])
            littlebird.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                                      datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(littlebird)
            logging.info('Logger re-enabled using configuration file settings.')
        except Exception as err:
            logging.warning(f'Error setting verbosity handler with type: {err.args}: {err}. Closing.')
            self.cleanexit(1)

        return

    def cleanexit(self, level):
        # Attempt to exit program cleanly by closing connections

        logging.shutdown()
        sys.exit(level)

    def setLogdir(self, path):

        if not os.path.exists(path):
            if query_yes_no(f'The path {path} does not exist.  Create it? [Y/n]'):
                try:
                    os.makedirs(path)
                    return True
                except Exception as err:
                    print(f'Error making directories: {err}')
                    return False
            else:
                return False


def query_yes_no(question, default="yes"):
    valid = {
        "yes": True,
        "ye": True,
        "y": True,
        "no": False,
        "n": False
    }
    if default is None:
        prompt = " [y/n]"
    elif default == "yes":
        prompt = " [Y/n]"
    elif default == "no":
        prompt = " [y/N]"
    else:
        raise ValueError(f'Invalid default answer: {default}')

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
