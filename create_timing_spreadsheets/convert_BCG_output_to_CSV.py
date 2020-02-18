# Joshua Smith
# 18/02/2020
# Takes the standard text output of a Enzo-E BiCGSTAB gravity simulation and converts it to a .csv spreadsheet
# containing: cycle start and finish times, solver iteration count, simulation time, and the number of blocks
# at each refinement level.


import re
import sys
import csv

### read in from console input ###############################################

fileName = sys.argv[1]   if len(sys.argv) > 1 else "test_output_BCG.txt"
outputFile = sys.argv[2] if len(sys.argv) > 2 else "test_output_BCG.csv"

lineList = []
with open(fileName, "r") as sourceFile:
    for line in sourceFile:
        lineList.append(line)

### Get iteration count and cycle end time (excluding print time) ############

# lines that start with B0 directly follow the end of a iteration cycle.
index_of_B0 = []
for i in range(len(lineList)):
    if re.match("^B0", lineList[i]):
        index_of_B0.append(i)

last_iter_index = [i - 1 for i in index_of_B0]

iteration_number = []
end_cycle_times = [] # end times exclude time taken to print.
for i in last_iter_index:
    words = lineList[i].split()
    iteration_number.append(int(words[5]))
    end_cycle_times.append(float(words[1]))

### Get cycle start time + sim time + cycle number ###########################

start_cycle_index = []
for i in range(len(lineList)):
    if re.search(".---$", lineList[i]):
        start_cycle_index.append(i + 1)

sim_times = []
start_cycle_times = []
cycle_number = []
for i in start_cycle_index:
    cycle_line = lineList[i].split()

    start_cycle_times.append(float(cycle_line[1]))
    cycle_number.append(int(cycle_line[4]))
    sim_times.append(float(lineList[i+1].split()[4]))

### Get number of blocks at each level + max level ###########################

max_level = 0
for i in range(len(lineList)):
    if re.search(".max_level", lineList[i]):
        max_level = int(lineList[i].split()[5])

block_index = []
for i in range(len(lineList)):
    if re.search(".level 0", lineList[i]):
        block_index.append(i)

# store number of blocks at each level in 2d array where [cycle][level]
blocks_at_level = [[0]*(max_level+1)]
for i in range(len(block_index)):
    zero_index = block_index[i]
    # initialise next list
    blocks_at_level.append([0]*(max_level+1))
    for level in range(max_level+1):
        blocks_at_level[i][level] = int(lineList[zero_index+level].split()[-1])




### Calculate time in python (for error checking) #############################

print_time = []
for i in range(1, len(start_cycle_times)):
    print_time.append(start_cycle_times[i] - end_cycle_times[i - 1])


cycle_time = []
for i in range(min(len(start_cycle_times), len(end_cycle_times))):
    cycle_time.append(end_cycle_times[i] - start_cycle_times[i])



### Export to csv file ###########################################################
#pad out lists that are one short by definition
iteration_number.append(None)
end_cycle_times.append(None)

rows = [([cycle_number[i],
         start_cycle_times[i],
         end_cycle_times[i],
         iteration_number[i],
         sim_times[i]]
        + blocks_at_level[i])
        for i in range(len(cycle_number))]

header = ["Cycle #",
          "Wall Time Start",
          "Wall Time End",
          "# of Iterations",
          "simulation time"]
header.extend(["# Blocks at level {}".format(i) for i in range(max_level+1)])

with open(outputFile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(header)
    writer.writerows(rows)

# prints if called from IDE #####################################################

if len(sys.argv) == 1: #assuming a console call would have arguments
    print("start cycle")
    print(start_cycle_times)
    print("end_cycle")
    print(end_cycle_times)
    print("iteration number")
    print(iteration_number)
    print("cycle number")
    print(cycle_number)
    print("simulation times")
    print(sim_times)
    print("max level = {}".format(max_level))
    print("blocks at level")
    print(blocks_at_level)
    print("time spent printing")
    print(print_time)
    print('time spent on cycle')
    print(cycle_time)