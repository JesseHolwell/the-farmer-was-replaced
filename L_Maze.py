from PGold import *

def runCondition():
	return num_items(Items.Gold) < 9863168

produceGoldAsync(runCondition)