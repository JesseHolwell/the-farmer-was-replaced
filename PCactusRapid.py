# Targeting the production achievement with bubble sort
# 67m per minute (not really)

from MProduceCactus import *

def runCondition(time):
	return get_time() - time < runtime

runtime = 1500
clear()
starting = num_items(Items.Cactus)
time = get_time()
while runCondition(time):
	produceCactusAsync()
	
ending = num_items(Items.Cactus)

quick_print("Produced", ending - starting, "in", runtime, "seconds")
	