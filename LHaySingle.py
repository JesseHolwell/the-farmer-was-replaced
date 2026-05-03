from RapidProduceHay import *

def runCondition():
	return num_items(Items.Hay) < 1000000000

produceHayAsync(runCondition)
	