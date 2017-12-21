import os
import sys

files = ["tours/annealing/temp-10000,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing/temp-1000000,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-100,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.001/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.007/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.020/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.08/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.200/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-10000,cooling-rate-0.400/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-100000,cooling-rate-0.001/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-100000,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-100000,cooling-rate-0.007/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-100000,cooling-rate-0.020/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.001/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.003/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.007/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.020/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.08/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.200/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/annealing_batch/temp-1000000,cooling-rate-0.400/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/genetic/mutations/swap-mutation,mutation-rate-0.005/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/genetic/mutations/swap-mutation,mutation-rate-0.015/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/genetic/mutations/swap-mutation,mutation-rate-0.035/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/genetic/mutations/swap-mutation,mutation-rate-0.035,init-pop-200/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/genetic/mutations/swap-mutation,mutation-rate-0.3/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/genetic/mutations/swap-mutation,mutation-rate-0.3,heavy/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/protected/tourAISearchfile" + sys.argv[1] + ".txt",
"tours/tourAISearchfile" + sys.argv[1] + ".txt"]


best_tour_files = []
best_tour_length = 10000000000000
for x in files:
	print("File: " + x)
	data_file = open(x, "r")
	data_text = data_file.read()
	data_file.close()
	data_split = [y.strip() for y in data_text.split("\n")]
	#os.system("cat " + x + " | grep LENGTH")
	#print(data_split)
	length = int(data_split[2][9:-1])
	if(length <= best_tour_length):
		best_tour_length = length
		best_tour_files.append(x)
	print("Tour length is: " + str(length))
	#print(data_split[1])
	print()
print()
print()
print()
print("Best tour had length " + str(best_tour_length))
print("Best tour files were:")
file_output = ""
for z in best_tour_files:
	print("\t" + z)
	file_output += z + "\n"

output_file = open("BEST_" + sys.argv[1] + ".txt", "w")
output_file.write(file_output)
output_file.close()