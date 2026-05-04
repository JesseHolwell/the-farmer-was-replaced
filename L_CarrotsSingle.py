from P_Carrots import *

def runCondition():
	return num_items(Items.Carrot) < 100000000

produceCarrots(runCondition)
	