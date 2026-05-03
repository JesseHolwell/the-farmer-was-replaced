from RapidProducePumpkins import *

def runCondition():
	return num_items(Items.Pumpkin) < 10000000

producePumpkinsAsync(runCondition)	