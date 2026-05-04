from P_Pumpkins import *
from P_Polyculture import *
from P_Sunflowers import *
from P_Cactus import *
from P_Maze import *
from P_Dinosaur import *
from P_Weird import *

weights = {
	Items.Hay:100,
	Items.Wood:1000,
	Items.Carrot:100, 
	Items.Pumpkin:100,
	Items.Weird_Substance:0.01,
	Items.Gold:10,
	Items.Power:0.01,
	Items.Cactus:100,
	Items.Bone:10,
}

def getLeast():
	resources = {
		Items.Hay,
		Items.Wood,
		Items.Carrot, 
		Items.Pumpkin,
		Items.Weird_Substance,
		Items.Gold,
		Items.Power,
		Items.Cactus,
		Items.Bone,
	}
	
	dict = {}
	
	for i in resources:
		dict[i] = num_items(i)

	lowest = 9999999999999999999999999
	lowestItem = None
	
	for i in resources:
		if (dict[i] / weights[i] < lowest):
			lowest = dict[i] / weights[i]
			lowestItem = i
	
	return lowestItem
	
def producePolyHay():
	producePolyculture(Entities.Grass)
	
def producePolyWood():
	producePolyculture(Entities.Tree)
	
def producePolyCarrots():
	producePolyculture(Entities.Carrot)
	
def produce(item):
	
	resources = {
		Items.Hay:producePolyHay,
		Items.Wood:producePolyWood,
		Items.Carrot:producePolyCarrots,
		Items.Pumpkin:producePumpkins,
		Items.Weird_Substance:produceWeird,
		Items.Gold:produceMaze,
		Items.Power:produceSunflowers,
		Items.Cactus:produceCactus,
		Items.Bone:produceDinosaur
	}
		
	return resources[item]

		
	
