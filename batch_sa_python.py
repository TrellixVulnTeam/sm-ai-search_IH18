### This file is used to batch loop through numerous different possibilities for the cooling rate and
### initial temperature parameters.

import os

list_of_nums = ["012", "017", "021", "026", "042", "048", "058", "175", "180", "535"]

for num in list_of_nums:
    #for i in range(7):
    # for i in ["0.0005", "0.0008", "0.0015", "0.0020", "0.0025",]:
    # for i in ["0.0001", "0.0002", "0.0003", "0.0004", "0.0006", "0.0007"]:
    # for i in ["0.001","0.003","0.007","0.020","0.08","0.200","0.400"]:
    for i in ["0.00005", "0.00007", "0.00009"]:
        initial_temp = "40000" #str(10 ** i)
        cooling_rate = i #"0.003"
        cmd = 'python simulated_annealing.py "duo_files/AISearchfile' + num + '.txt" "tours/annealing_batch_NEW/temp-' + initial_temp + ',cooling-rate-' + cooling_rate + '/tourAISearchfile' + num + '.txt" ' + initial_temp + ' ' + cooling_rate
        print()
        print("EXECUTING:\n" + cmd)
        print()
        os.system(cmd)
