# Standard Library Imports
import pymongo
import logging
# Locally Developed Imports

# Third Party Imports


class mongoLB:

    def __init__(self, config):
        self.connect = self.connect_db(config)
        self.dbc = self.connect['Littlebird']
        self.__validtype = {"discorduser": self.dbc.discorduser, "xivdata": self.dbc.xivdata,
                 "div2data": self.dbc.div2data, "brp": self.dbc.div2data,
                 "randomdata": self.dbc.randomdata}

    def connect_db(self, config):
        try:
            mongouri = "mongodb://" + config["HOST"] + ":" + str(config["PORT"]) + "/"
            logging.info(f'Connecting to {mongouri}')
            return pymongo.MongoClient(mongouri)
        except Exception as err:
            logging.warning(f'Cannot connect to database.  Please check your settings.')
            return None

    def push_document(self, doctype, content):

        if doctype not in self.__validtype:
            logging.warning(f'Document type {doctype} not supported.')
            return None
        else:
            pushdoc = self.__validtype[doctype]
            pushdoc_id = pushdoc.insert_one(content).inserted_id
            logging.info(f'Pushing document of type {doctype} to database as doctype {pushdoc_id["_id"]}')
            return pushdoc_id

    def get_document(self, doctype, ref):

        if doctype not in self.__validtype:
            logging.warning(f'Document type {doctype} not supported.')
            return None
        else:
            pulldoc = self.__validtype[doctype]
            pulled = pulldoc.find_one(ref)
            logging.info(f'Pushing document of type {doctype} to database as doctype {pulled["_id"]}')
            return pulled


