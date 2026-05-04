from P_Wood import *

def runCondition():
	return num_items(Items.Wood) < 500000000

produceWood(runCondition)