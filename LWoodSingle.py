from RapidProduceWood import *

def runCondition():
	return num_items(Items.Wood) < 500000000

produceWoodAsync(runCondition)