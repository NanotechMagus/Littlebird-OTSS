# Standard Library Imports
import requests
import logging
import json

# Locally Developed Imports

# Third Party Imports


class DivTech:

    def __init__(self, discorduser):
        self.user = discorduser
        self.pid = None
        self.content = {}

    def getnewplayer(self, platform, name):

        parameter = {"name": name, "platform": platform}

        try:
            data = requests.get("https://thedivisiontab.com/api/search.php", params=parameter)

            if not data.status_code == 200:
                raise data.status_code
            else:
                dataname = data.content
                dataname = json.loads(dataname)
                self.setPlayerContent(dataname['results'][0])
        except Exception as err:
            # logging.WARN(f'Error connecting to SHDTech resources. {err}')
            raise err

        return

    def setPlayerContent(self, playercontent, pid=None):

        if playercontent['pid']:
            self.pid = playercontent['pid']
            self.content = playercontent
            self.setDatabaseEntry()
        elif pid:
            self.pid = pid
            self.content = playercontent
            self.setDatabaseEntry()
        else:
            logging.WARN('Error: player information not found; database not updated.')

        return

    def setDatabaseEntry(self):

        return

    def getcontentpid(self, pid):

        param = {"pid": pid}

        try:
            data = requests.get("https://thedivisiontab.com/api/player.php", params=param)

            if not data.status_code == 200:
                raise data.status_code
            else:
                dataname = data.content
                self.setPlayerContent(json.loads(dataname))
        except Exception as err:
            logging.WARN(f'Error connecting to SHDTech resources. {err}')
            raise err

        return
