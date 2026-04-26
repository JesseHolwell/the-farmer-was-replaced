from ProducePumpkins import *
from ProduceMain import *
from ProducePower import *
from ProduceCactus import *
from ProduceGold import *
from ProduceBone import *

weights = {
	Items.Hay:100,
	Items.Wood:1000,
	Items.Carrot:100, 
	Items.Pumpkin:100,
	#Items.Weird_Substance:1,
	Items.Gold:10,
	Items.Power:1,
	Items.Cactus:100,
	Items.Bone:10,
}

def getLeast():
	resources = {
		Items.Hay,
		Items.Wood,
		Items.Carrot, 
		Items.Pumpkin,
		#Items.Weird_Substance,
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
	
def produce(item):
	
	resources = {
		Items.Hay:producePolyculture,
		Items.Wood:producePolyculture,
		Items.Carrot:producePolyculture,
		Items.Pumpkin:producePumpkins,
		#Items.Weird_Substance:clear,
		Items.Gold:produceGold,
		Items.Power:producePower,
		Items.Cactus:produceCactus,
		Items.Bone:produceBone
	}
		
	return resources[item]
		
	
