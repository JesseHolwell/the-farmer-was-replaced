# Targeting the production achievement farming descending order
# 12k per minute

from MProducePower import *

def runCondition(time):
	return get_time() - time < runtime

runtime = 180
clear()
startingPower = num_items(Items.Power)
time = get_time()
while runCondition(time):
	producePowerAsync()
	
endingPower = num_items(Items.Power)

quick_print("Produced", endingPower - startingPower, "in", runtime, "seconds")
	