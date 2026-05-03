from P_Pumpkins import *

def runCondition():
	return num_items(Items.Pumpkin) < 200000000

producePumpkinsAsync(runCondition)	