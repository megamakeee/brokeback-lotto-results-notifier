"""
    Script to get the latest lotto numbers and send notification
    of the results.

"""

import lottoFunctions as lf

# The Script #

# Basic variables
numbers_file = "numbers.csv"

# Process itself
lotto_results = lf.get_latest_lotto_results()
print(lotto_results)

lotto_lines = lf.get_own_lotto_lines_to_list_of_lists(numbers_file)
print(lotto_lines)
