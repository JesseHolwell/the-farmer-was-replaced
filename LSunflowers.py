from RapidProduceSunflowers import *

def runCondition():
	return num_items(Items.Power) < 100000

produceSunflowersAsync(runCondition)		