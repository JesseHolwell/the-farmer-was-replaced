from RapidProduceSunflowers import *

def runCondition():
	return num_items(Items.Power) < 10000

produceSunflowersAsync(runCondition)		
	