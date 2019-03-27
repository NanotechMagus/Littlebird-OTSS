# Standard Library Imports
import requests
import json
import logging
from urllib.parse import urljoin

# Locally Developed Imports

# Third Party Imports


class DivTech:

    def __init__(self):
        self.__api = "https://thedivisiontab.com/api/"

    def search_by_name(self, platform, name):

        try:

            if not validate_me("shd_platform", platform.lower()):
                raise ValueError(f'{platform} cannot be found in SHDTech API.')
            else:
                parameter = {"name": name.lower(), "platform": platform.lower()}

            data = requests.get(urljoin(self.__api, "search.php"), params=parameter)

            if not data.status_code == requests.codes.ok:
                raise ValueError(f'{data.status_code} received. Cannot connect to SHDTech API')

            datac = json.loads(data.content)

            if datac['totalresults'] >= 1:
                for items in datac['results']:
                    if items['name'] == name:
                        return items
            else:
                raise AttributeError(f'Could not find {name} on {platform}')

        except ValueError as err:
            logging.warning(f'{err}')
            return None
        except AttributeError as err:
            logging.warning(f'{err}')

    def search_by_pid(self, pid):

        try:
            if pid:
                parameter = {"pid": pid}
            else:
                raise AttributeError(f'Invalid pid: {pid}')

            data = requests.get(urljoin(self.__api, "player.php"), params=parameter)

            if not data.status_code == requests.codes.ok:
                raise ValueError(f'{data.status_code} received. Cannot connect to SHDTech API')

            shd_data = json.loads(data.content)

            if not shd_data['playerfound']:
                raise KeyError(f'Player not found with pid: {pid}')
            else:
                return shd_data

        except AttributeError as err:
            logging.warning(err)
            return None
        except ValueError as err:
            logging.warning(err)
            return None


class xivAPI:

    def __init__(self, key=None):
        self.__api = "https://xivapi.com/"
        self.__key = key

    def init_api(self, getinit="default"):

        content = requests.get(urljoin(self.__api, "content"))
        server = requests.get(urljoin(self.__api, "servers"))
        dc = requests.get(urljoin(self.__api, "servers/dc"))

        initial_list = {
            "xivcontentlist": json.loads(content.content),
            "xivserverlist": json.loads(server.content),
            "xivdclist": json.loads(dc.content)
        }

        if getinit == "default":
            return initial_list
        elif getinit in initial_list:
            return initial_list[getinit]
        else:
            return None

    def get_id(self, name, server, stype="char"):

        try:

            if not validate_me("csearch", stype):
                raise NameError(f'{stype} is not a valid search type.')
            else:
                params = {"name": name, "server": server}
            logging.info(f'Attempting to contact server at '
                         f'{urljoin(self.__api, validate_me("csearch", stype) + "/search")}')
            search = requests.get(urljoin(self.__api, validate_me("csearch", stype) + "/search"), params=params)

            if not search.status_code == requests.codes.ok:
                raise ValueError(f'Their server is taking a break, status code: {search.status_code}')

            usearch = json.loads(search.content)

            if usearch['Pagination']['ResultsTotal'] >= 1:
                for charname in usearch['Results']:
                    if charname['Name'] == name:
                        return charname['ID']
            else:
                raise KeyError(f'Cannot find character {name} on server {server}')

        except KeyError as err:
            logging.info(err)
            return err
        except NameError as err:
            logging.warning(err)
            return err
        except ValueError as err:
            logging.warning(err)
            return err

    def get_full_char_info(self, stype, pid):

        try:
            params = {"data": "FC,PVP"}
            charinfo = requests.get(urljoin(self.__api, validate_me("csearch", stype) + "/" + str(pid)), params=params)
            logging.warning(f'Performed search at {charinfo.url}')

            if not charinfo.status_code == requests.codes.ok:
                raise ValueError(f'There server is taking a break, status code: {charinfo.status_code}')

            usearch = json.loads(charinfo.content)

            if not usearch['Info']['Character']['State'] == 2:
                raise AttributeError(f"{validate_me('cstate', usearch['Info']['Character']['State'])}")
            else:
                return usearch
        except ValueError as err:
            logging.warning(f'{err}')
            return None
        except AttributeError as err:
            logging.warning(f'{err}')
            return None

    def get_content_info(self, ctype, id):

        try:

            print(f'Pulling information from {urljoin(self.__api, ctype + "/" + str(id))}.')
            data = requests.get(urljoin(self.__api, ctype + "/" + str(id)))

            return json.loads(data.content)

        except ValueError as err:
            logging.warning(err)


def validate_me(vtype, vcontent):
    vtypes = {
        "cstate":
            {
                0: 'Content is not on XIVAPI and will not be added via this request',
                1: 'Content does not exist on the API and needs adding. The Payload should be empty if this '
                   'state is provided. It should take 2 minutes or less to add the content.',
                3: 'Content does not exist on The Lodestone.',
                4: 'Content has been Blacklisted. No data can be obtained via the API for any application.',
                5: 'Content is private on lodestone, ask the owner to make the content public and then try again!'
            },
        "csearch":
            {
                "char": "character",
                "ls": "linkshell",
                "fc": "freecompany",
                "pvpt": "pvpteam",
            },
        "shd_platform":
            {
                "xbox": "xbl",
                "xbone": "xbl",
                "xb": "xbl",
                "xbl": "xbl",
                "playstation": "psn",
                "ps4": "psn",
                "ps": "psn",
                "psn": "psn",
                "uplay": "uplay",
                "pc": "uplay"
            }
    }

    try:
        if vtype not in vtypes:
            raise AttributeError(f'{vtype} not in validated list of responses.')
        elif vcontent not in vtypes[vtype]:
            raise KeyError(f'{vcontent} not a valid content property.')
        else:
            return vtypes[vtype][vcontent]

    except AttributeError as err:
        logging.warning(err)
        return None
    except KeyError as err:
        logging.warning(err)
        return None

