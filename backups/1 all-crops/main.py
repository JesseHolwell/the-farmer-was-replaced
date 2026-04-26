from Orchestration import *

while True:
	leastItem = getLeast()
	
	function = produce(leastItem)
	
	function()
	