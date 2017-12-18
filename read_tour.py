# -- File: read_tour.py --
# Author: vzbf32
# Creation Date: 2017-12-18 21:20
# Purpose: This script loads tour text files, as required for the assignment, and stores them in a suitable data format.


def die(err):
    print("Error:", err)


file_path = "duo_files/AISearchfile012.txt"
data_file = open(file_path, "r")
data_text = data_file.read()
data_file.close()

split = [x.strip() for x in data_text.replace(" ", "").split(",")]
print(split)

name = ""
size = -1

# Check the first element is "NAME = xxx"
if not split[0].startswith("NAME="):
    die("Did not start with NAME = ")
elif not split[1].startswith("SIZE="):
    die("Second element did not have SIZE = ")
else:
    name = split[0][5:]
    size = int(split[1][5:])
    print("Successful")
    print("Name:", name)
    print("Size:", size)

