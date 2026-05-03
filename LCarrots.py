from RapidProduceCarrots import *

def runCondition():
	return num_items(Items.Carrot) < 2000000000

produceCarrotsAsync(runCondition)