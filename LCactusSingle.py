from RapidProduceCactus import *

def runCondition():
	return num_items(Items.Cactus) < 131072

produceCactusAsync(runCondition)		
	