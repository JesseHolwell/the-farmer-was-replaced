
map = {
	Items.Hay:"SHay",
	Items.Wood:"SWood",
	Items.Carrot:"SCarrot",
	Items.Pumpkin:"SPumpkin",
	Items.Cactus:"SCactus",
	Items.Power:"SSunflower",
	Items.Bone:"SBone",
	Items.Weird_Substance:"SWeird",
	Items.Gold:"SGold"
}
sim_unlocks = Unlocks
sim_items = {
	Items.Hay:1000000000,
	Items.Wood:1000000000,
	Items.Carrot:1000000000,
	Items.Pumpkin:1000000000,
	Items.Cactus:1000000000,
	Items.Power:1000000000,
	Items.Bone:1000000000,
	Items.Weird_Substance:1000000000,
	Items.Gold:1000000000,
	Items.Water:1000000000,
	Items.Fertilizer:1000000000
}
sim_globals = {}
seed = 0
speedup = 1000

target = Items.Hay

run_time = simulate(map[target], sim_unlocks, sim_items, sim_globals, seed, speedup)