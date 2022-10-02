"""do stuff"""

import json

import requests
import urllib3

from modules import constants as con

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_data() -> json:
    """get the stuff"""

    res = requests.post(con.AUTH_URL, data=con.REQUEST_DATA, verify=False)
    access_token = res.json()["access_token"]
    header = {"Authorization": f"Bearer {access_token}"}
    param = {"per_page": 200, "page": 1}

    return requests.get(con.ACTIVITIES_URL, headers=header, params=param).json()
