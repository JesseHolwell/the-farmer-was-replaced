def benchmark(target, function):
	runTime = 60
	runItems = 1000
		
	startItems = num_items(target)
	startTime = get_time()
	
	def runConditionTime():
		return get_time() - startTime < runTime
		
	def runConditionItems():
		return num_items(target) - startItems < runItems
		
	function(runConditionTime)
	#function(runConditionItems)
			
	endItems = num_items(target)
	endTime = get_time()
	
	totalTime = endTime - startTime
	totalItems = endItems - startItems
	
	inMinutes = totalTime / 60
	perMinute = totalItems / 60
			
	quick_print(target, "produced", totalItems, "in", totalTime, "seconds")
	quick_print("averaged", perMinute, "per minute")