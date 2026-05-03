from RapidProduceHay import *

def runCondition():
	return num_items(Items.Hay) < 2000000000

produceHayAsync(runCondition)
	