from P_Wood import *

def runCondition():
	return num_items(Items.Wood) < 10000000000

produceWoodAsync(runCondition)
	