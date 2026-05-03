
filename = "RapidProduceHay"
sim_unlocks = Unlocks
sim_items = {Items.Hay:100000999999999, Items.Wood:1000009999999, Items.Power: 1000000000}
sim_globals = {}
seed = 0
speedup = 1000

run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)