from P_Hay import *

def runCondition():
	return num_items(Items.Hay) < 2000000000

produceHay(runCondition)
	