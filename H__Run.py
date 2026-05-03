from H_Orchestration import *
from H_Statistics import *

change_hat(Hats.Top_Hat)

while True:
	leastItem = getLeast()
	
	function = produce(leastItem)

	runWithStats(function, leastItem)
	