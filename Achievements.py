unlockedHats = [
Hats.Brown_Hat,
Hats.Cactus_Hat,
Hats.Carrot_Hat,
Hats.Gold_Hat,
Hats.Gray_Hat,
Hats.Green_Hat
]

def equipHat():
	
	hatsLength = len(unlockedHats)

	index = random() * hatsLength // 1
	
	i = 0
	for x in unlockedHats:
		if i == index:
			change_hat(x)
			
		i += 1
		
	while True:
		do_a_flip()

for i in range(max_drones()):
	move(East)
	spawn_drone(equipHat)