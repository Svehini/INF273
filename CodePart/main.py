from runner import * 

# ALL FILES
files = ['Call_7_Vehicle_3.txt', 'Call_18_Vehicle_5.txt', 'Call_35_Vehicle_7.txt', 
         'Call_80_Vehicle_20.txt', 'Call_130_Vehicle_40.txt', 'Call_300_Vehicle_90.txt']

# files = ['Call_7_Vehicle_3.txt', 'Call_18_Vehicle_5.txt', 'Call_35_Vehicle_7.txt']

# files = ['Call_300_Vehicle_90.txt']
# files = ['Call_80_Vehicle_20.txt']
# files =  ['Call_35_Vehicle_7.txt']
# files = ['Call_7_Vehicle_3.txt']

# type = "Random"
# type = "Local"
type = "SimAnn"

repeats = 10000
rounds = 10

print(runnerFunc(files, rounds, repeats, type))



# [0, 0, 6, 6, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 7, 7]

