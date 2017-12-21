import os
# os.system("dir")
# os.system("type batch_loop_sa.bat")

list_of_nums = ["012", "017", "021", "026", "042", "048", "058", "175", "180", "535"]

# list_of_files = [
#         "duo_files/AISearchfile012.txt",
#         "duo_files/AISearchfile017.txt",
#         "duo_files/AISearchfile021.txt",
#         "duo_files/AISearchfile026.txt"#,
#         "duo_files/AISearchfile042.txt",
#         "duo_files/AISearchfile048.txt",
#         "duo_files/AISearchfile058.txt",
#         "duo_files/AISearchfile175.txt",
#         "duo_files/AISearchfile180.txt",
#         "duo_files/AISearchfile535.txt"
#     ]

for num in list_of_nums:
    #for i in range(7):
    for i in ["0.001","0.003","0.007","0.020","0.08","0.200","0.400"]:
        initial_temp = "10000" #str(10 ** i)
        cooling_rate = i #"0.003"
        cmd = 'python simulated_annealing.py "duo_files/AISearchfile' + num + '.txt" "tours/annealing_batch/temp-' + initial_temp + ',cooling-rate-' + cooling_rate + '/tourAISearchfile' + num + '.txt" ' + initial_temp + ' ' + cooling_rate
        print()
        print("EXECUTING:\n" + cmd)
        print()
        os.system(cmd)
