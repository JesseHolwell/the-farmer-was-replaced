from P_Cactus import *

def runCondition():
	return num_items(Items.Cactus) < 33554432

produceCactusAsync(runCondition)		
	