from P_Maze import *

def runCondition():
	return num_items(Items.Gold) < 616448

produceMaze(runCondition)
	