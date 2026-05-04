from P_Sunflowers import *

def runCondition():
	return num_items(Items.Power) < 10000

produceSunflowers(runCondition)	