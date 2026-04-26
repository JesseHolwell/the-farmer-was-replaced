from Orchestration import *
from Statistics import *

while True:
	leastItem = getLeast()
	
	function = produce(leastItem)

	runWithStats(function, leastItem)
	