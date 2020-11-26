import requests
import json
import time
import datetime
import os
from twilio.rest import Client
from csv import reader


def get_latest_lotto_results():
    """
    Function to get the latest lotto results

    """

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
            return r.json()[0]["results"][0]["primary"] + r.json()[0]["results"][0]["secondary"] + r.json()[0]["results"][0]["tertiary"]
        else:
            raise Exception("Empty result set", 69)
    else:
        raise Exception("API query failed", r.status_code)


def get_own_lotto_lines_to_list_of_lists(filename):
    """
    Function to read own lottery numbers to list of lists

    """

    # read csv file as a list of lists
    with open(filename, 'r') as read_obj:
        # Pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        return list_of_rows


def send_sms(to_number, from_number, message):
    """
    Function to send SMS

    """
    account_sid = os.environ.get('twilio_account_sid')
    auth_token = os.environ.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                from_=from_number,
                                body=message,
                                to=to_number
                            )
