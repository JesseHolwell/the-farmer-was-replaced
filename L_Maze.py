from P_Maze import *

def runCondition():
	return num_items(Items.Gold) < 9863168

produceMaze(runCondition)