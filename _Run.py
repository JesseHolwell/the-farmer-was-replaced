from H_Orchestration import *
from H_Statistics import *

while True:
	leastItem = getLeast()
	
	function = produce(leastItem)

	runWithStats(function, leastItem)
	