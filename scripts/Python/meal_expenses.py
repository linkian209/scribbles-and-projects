import numpy as np
from prettytable import PrettyTable

# Get inputs from user
amount = 0
days = 0
max_threshold = 0
tolerance = 0

# Get input parameters
loop = False
while not loop:
	amount = input('Enter total amount without dollar sign: ')
	try:
		amount = float(amount)
		loop = True
	except:
		print('Invalid input [{}].'.format(amount))

loop = False
while not loop:
	days = input('Enter number of days: ')
	try:
		days = int(days)
		loop = True
	except:
		print('Invalid input [{}].'.format(days))

loop = False
while not loop:
    max_threshold = input('Enter max threshold for single day: ')
    try:
        max_threshold = float(max_threshold)
        loop = True
    except:
        print('Invalid input [{}].'.format(max_threshold))

loop = False
while not loop:
    tolerance = input('Enter tolerance (in standard deviations) for a single day: ')
    try:
        tolerance = float(tolerance)
        loop = True
    except:
        print('Invalid input [{}].'.format(tolerance))
# Generate numbers and make sure no number is above the max threshold
loop = False
while not loop:
    # Get this run's set
    base_nums = [x * amount for x in np.random.dirichlet(np.ones(days))]
    
    # Calculate statistics
    set_average = np.average(base_nums)
    set_std = np.std(base_nums)
    upper_lim = set_average + (set_std * tolerance)
    lower_lim = set_average - (set_std * tolerance)
    
    # Loop through each number and make sure none are greater than the max 
    # threshold and are within tolerance
    num_greater = False
    num_oot = False
    for num in base_nums:
        if num > max_threshold:
            num_greater = True
            break
            
        if num > upper_lim or num < lower_lim:
            num_oot = True
            break

    # Check if we have a number greater
    if num_greater or num_oot:
        continue
    else:
        rounded = [round(x, 2) for x in base_nums]
        loop = True

# Output numbers 
table = PrettyTable()
table.add_column("Day #", range(days))
table.add_column("Base Amount", base_nums)
table.add_column("Rounded Amount", rounded)
print(table)

table = PrettyTable()
table.add_column("Average", [set_average])
table.add_column("Standard Deviation", [set_std])
table.add_column("Upper Limit", [upper_lim])
table.add_column("Lower Limit", [lower_lim])
print(table)

# Print Complete and show end statistics
print('Done. Generated {} numbers summing to {} ({} rounded)'.format(days, sum(base_nums), sum(rounded)))