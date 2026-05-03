def runWithStats(function, item):

	quick_print("producing: ", item, "with", function)
	beforeItems = num_items(item)
	beforeTime = get_time()
	
	function()
	
	afterItems = num_items(item)
	afterTime = get_time()
	
	producedItems = afterItems - beforeItems
	productionTime = afterTime - beforeTime
	
	quick_print("produced:", producedItems,
		"in", productionTime)
		
	quick_print("ips:", producedItems / productionTime)
	
	
	
	