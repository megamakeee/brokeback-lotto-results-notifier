"""
    Script to get the latest lotto numbers and send notification
    of the results.

"""

import lottoFunctions as lf

# The Script #

# Basic variables
numbers_file = "numbers.csv"

# Process itself

# Get the current draw
current_draw = lf.get_latest_lotto_draw()
print(current_draw)

# Get your own played lines
played_lines = lf.get_own_lotto_lines_to_list_of_sets(numbers_file)
print(played_lines)

# Check the results
results = lf.check_results(current_draw, played_lines)
print(results)

# If there are wins get the prizes
