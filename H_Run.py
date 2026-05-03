from Orchestration import *
from Statistics import *

change_hat(Hats.Top_Hat)

while True:
	leastItem = getLeast()
	
	function = produce(leastItem)

	runWithStats(function, leastItem)
	