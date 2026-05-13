from P_Starter import *
from P_Hay import *
from P_Wood import *
from P_Carrots import *
from P_Pumpkins import *
from P_Polyculture import *
from P_Sunflowers import *
from P_Cactus import *
from P_Maze import *
from P_Dinosaur import *
from P_Weird import *

initialMap = {
	Unlocks.Speed:produceHaySingle,
	Unlocks.Expand:produceBushes,
	Unlocks.Plant:produceCarrots,
	Unlocks.Carrots:produceTriplet
}

perPlantSeedCost = {
	Items.Hay:{},
	Items.Wood:{},
	Items.Carrot:get_cost(Entities.Carrot),
	Items.Pumpkin:get_cost(Entities.Pumpkin),
	Items.Weird_Substance:{},
}

def noProducer(runCondition):
	pass

def selectProducer(item):
	if item == Items.Hay:
		if num_unlocked(Unlocks.Polyculture) > 0:
			return produceHay
		if num_unlocked(Unlocks.Carrots) > 0:
			return produceTriplet
		return produceHaySingle
	if item == Items.Wood:
		if num_unlocked(Unlocks.Polyculture) > 0:
			return produceWood
		if num_unlocked(Unlocks.Carrots) > 0:
			return produceTriplet
		if num_unlocked(Unlocks.Plant) > 0:
			return produceBushes
		return noProducer
	if item == Items.Carrot:
		if num_unlocked(Unlocks.Polyculture) > 0:
			return produceCarrots
		if num_unlocked(Unlocks.Carrots) > 0:
			return produceTriplet
		return noProducer
	return produce(item)

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
		Items.Hay:produceHay,
		Items.Wood:produceWood,
		Items.Carrot:produceCarrots,
		Items.Pumpkin:producePumpkins,
		Items.Weird_Substance:produceWeird,
		Items.Gold:produceMaze,
		Items.Power:produceSunflowers,
		Items.Cactus:produceCactus,
		Items.Bone:produceDinosaur
	}
		
	return resources[item]

		
	
