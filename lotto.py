"""
    Script to get the latest lotto numbers and send notification
    of the results.

"""

import lottoFunctions as lf
import os

# The Script #

# Basic variables
lotto_numbers_file = "numbers.csv"
phone_numbers_file = "phonenumbers.csv"

# Process itself

# Get the current draw
current_draw = lf.get_latest_lotto_draw()
# print(current_draw)

# Get the prize tiers
prizeTiers = lf.get_prize_tiers()
# print(prizeTiers)

# Get your own played lines
played_lines = lf.get_own_lotto_lines_to_list_of_sets(lotto_numbers_file)
# print(played_lines)

# Get phonenumbers
phonenumbers = lf.get_phonenumbers(phone_numbers_file)
# print(phonenumbers)

# Check the results
results = lf.check_results(current_draw, played_lines)
# print(results)

# Formulate the message
message = lf.formulate_message(results, prizeTiers)
# print(message)

# Send the formulated message of weeks results to the phonenumbers in phone_numbers_file
for phonenumber in phonenumbers:
    print(f"lf.send_sms({phonenumber[0]},{os.environ.get('twilio_from_number')},\"{message}\")")
    lf.send_sms(phonenumber[0], os.environ.get('twilio_from_number'), message)
