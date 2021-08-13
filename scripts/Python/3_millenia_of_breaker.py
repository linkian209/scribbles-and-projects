import math

# Starting calculations
print('Running Starting calculations...')
num_millenia = 3.0
meters_per_spool = 300.0
seconds_per_spool = 150.0 * 60.0
breaker_thickness = .01
print('Assuming the following: ')
print('Meters per Spool: {}m'.format(meters_per_spool))
print('Cycle Time: {}s\n'.format(seconds_per_spool))

# Total amount of breaker is number of seconds in millenia divided by
# the number of seconds per spool, multiplied by meters per spool
total_breaker = meters_per_spool * (num_millenia * 1000 * 365.25 * 24.0 * 3600.0) / seconds_per_spool
				
print('Total breaker required: {} meters\n'.format(total_breaker))

# Calculate the size of the roll
start_roll_radius = .5
total_spooled = 0.0
num_loops = 0

print('Spooling breaker...')
print('Assuming breaker thickness of {}m and starting radius of {}m'.format(breaker_thickness,start_roll_radius))

while total_spooled < total_breaker:
    # To get amount spooled on this loop, we add the circumference
    cur_loop = 2.0 * math.pi * (start_roll_radius + (num_loops * breaker_thickness))
    
    # If the current loop is more than what is remaining, only add what is left
    if cur_loop < total_breaker - total_spooled:
        total_spooled += cur_loop
    else:
        total_spooled += total_breaker - total_spooled

    num_loops += 1
	
print('Spooling Complete')
print('Total number of loops: {}'.format(num_loops))
print('Spool Radius: {}m'.format(start_roll_radius + (num_loops * breaker_thickness)))