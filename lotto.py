"""
    Script to get the latest lotto numbers and send notification
    of the results.

"""

# Libraries needed
import requests
import json
import time
import datetime

"""
    Function to get the latest lotto results

"""


def get_latest_lotto_results():
    # Set host
    baseURL = "https://www.veikkaus.fi"
    endpointURL = "/api/draw-results/v1/games/LOTTO/draws/by-week/"
    year = str(datetime.date.today().isocalendar()[0])
    # Week number has -1 to get some results whenever script is run
    week = str(datetime.date.today().isocalendar()[1] - 1)
    api_url = baseURL + endpointURL + year + "-W" + week

    # Set headers
    headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-ESA-API-Key': 'ROBOT'
    }

    # Create a session
    s = requests.Session()

    # Get the lotto results
    r = s.get(api_url, headers=headers)

    if r.status_code == 200:
        if len(r.json()) > 0:
            return r.json()[0]
        else:
            raise Exception("Empty result set", 69)
    else:
        raise Exception("API query failed", r.status_code)


lotto_results = get_latest_lotto_results()

print(lotto_results)
