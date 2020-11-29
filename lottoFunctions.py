import requests
import json
import time
import datetime
import os
from twilio.rest import Client
from csv import reader


def get_latest_lotto_draw():
    """
    Function to get the latest lotto results

    """

    # Set host
    baseURL = "https://www.veikkaus.fi"
    endpointURL = "/api/draw-results/v1/games/LOTTO/draws/by-week/"
    year = str(datetime.date.today().isocalendar()[0])
    # Week number has -1 to get some results whenever script is run
    week = str(datetime.date.today().isocalendar()[1])
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
            ret = []
            primary_numbers = set(r.json()[0]["results"][0]["primary"])
            secondary_number = set(r.json()[0]["results"][0]["secondary"])
            tertiary_number = set(r.json()[0]["results"][0]["tertiary"])
            ret.append(primary_numbers)
            ret.append(secondary_number)
            ret.append(tertiary_number)

            return ret
        else:
            raise Exception("Empty result set", 69)
    else:
        raise Exception("API query failed", r.status_code)


def get_own_lotto_lines_to_list_of_sets(filename):
    """
    Function to read own lottery numbers to list of lists

    """

    # read csv file as a list of lists
    with open(filename, 'r') as read_obj:
        # Pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)

    list_of_sets = []

    for x in list_of_rows:
        list_of_sets.append(set(x))

    return list_of_sets


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


def check_results(current_draw, played_lines):
    """
    Function to check the results

    """
    results = []
    primary_numbers = current_draw[0]
    secondary_number = current_draw[1]

    for row in played_lines:
        correct_primary_numbers = len(primary_numbers.intersection(row))
        correct_secondary_numbers = len(secondary_number.intersection(row))

        if correct_primary_numbers == 3 and correct_secondary_numbers > 0:
            result = f"{correct_primary_numbers}+{correct_secondary_numbers}"
            results.append(result)
        elif correct_primary_numbers >= 4 and correct_primary_numbers <= 6:
            result = f"{correct_primary_numbers}"
            results.append(result)
        elif correct_primary_numbers == 6 and correct_secondary_numbers > 0:
            result = f"{correct_primary_numbers}+{correct_secondary_numbers}"
            results.append(result)
        elif correct_primary_numbers == 7:
            result = f"{correct_primary_numbers}"
            results.append(result)

    results.sort()
    return results


def formulate_message(results, prizes):
    message = f"BROKEBACK LOTTO\n"
    if len(results) > 0:
        message += f"Hyvä jätkät, hienosti!\nTällä viikolla kupongissa oli "
        counter = 1
        winnings = 0
        for result in results:
            winnings += prizes[result]
            if counter == len(results[:-1]) and len(results) > 1:
                message += f"{result} "
            elif counter < len(results) and len(results) > 1:
                message += f"{result}, "
            elif counter == len(results) and len(results) > 1:
                message += f"ja {result}"
            elif counter == len(results) and len(results) == 1:
                message += f"{result}"
            counter += 1
        winnings = str(winnings).replace(".", ",")
        message += f" oikein.\nVoititte yhteensä {winnings} euroa!"
    else:
        message += "Pirskatti! Ei voittoa lotossa tällä viikolla."

    return message


def get_prize_tiers():
    # Set host
    baseURL = "https://www.veikkaus.fi"
    endpointURL = "/api/draw-results/v1/games/LOTTO/draws/by-week/"
    year = str(datetime.date.today().isocalendar()[0])
    # Week number has -1 to get some results whenever script is run
    week = str(datetime.date.today().isocalendar()[1])
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
            prizeTiers = r.json()[0]["prizeTiers"]
            # Pick only the 6 first prize tiers, that does not include doubling or plus number prizes.
            prizeTiers = prizeTiers[:6]
            prizes = {}
            for prize in prizeTiers:
                prizes[prize["name"].replace(' oikein', '')] = prize["shareAmount"] / 100
            return prizes
        else:
            raise Exception("Empty result set", 69)
    else:
        raise Exception("API query failed", r.status_code)


def get_phonenumbers(filename):
    """
    Function to read phonenumbers to list

    """

    # read csv file as a list of lists
    with open(filename, 'r') as read_obj:
        # Pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)

    return list_of_rows
