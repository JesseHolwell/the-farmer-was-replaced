from PGold import *

def runCondition():
	return num_items(Items.Gold) < 616448

produceGoldAsync(runCondition)
	