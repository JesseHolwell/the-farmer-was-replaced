# Targeting the production achievement farming map filled pumpkin
# 20m per minute

from MProducePumpkins import *
from MovementAsync import *


def runCondition(time):
	return get_time() - time < runtime

runtime = 120
clear()
#tillFieldAsync()

#while (num_drones() != 1):
#	do_a_flip()
	
startingPumpkins = num_items(Items.Pumpkin)

time = get_time()
while runCondition(time):
	producePumpkinsAsync()
	
endingPumpkins = num_items(Items.Pumpkin)

quick_print("Produced", endingPumpkins - startingPumpkins, "in", runtime, "seconds")
	