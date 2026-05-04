from P_Sunflowers import *

def runCondition():
	return num_items(Items.Power) < 100000

produceSunflowers(runCondition)		