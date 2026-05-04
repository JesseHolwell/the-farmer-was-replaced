from P_Pumpkins import *

def runCondition():
	return num_items(Items.Pumpkin) < 10000000

producePumpkins(runCondition)	