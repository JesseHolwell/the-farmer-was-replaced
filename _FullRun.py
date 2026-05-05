from H_FullRun import *

def target(unlockItem):
	unlockCondition = getRunCondition(unlockItem)

	# if already unlocked, move along
	if unlocked(unlockItemKey):
		return
	else:
		unlockFunction = getFunction(unlockItem)
		unlockFunction(unlockCondition)
	
	# else, get the matching function
	unlock(unlockItemKey)

target({Unlocks.Loops:1})
target({Unlocks.Speed:1})
target({Unlocks.Expand:1})
target({Unlocks.Plant:1})
target({Unlocks.Carrots:1})
	

	

