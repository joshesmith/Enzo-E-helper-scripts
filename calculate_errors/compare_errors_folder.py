import sys
import os
import math

from compare_errors import compare_data_files

if __name__ == "__main__":
    # take optional input from system arguments
    good_directory = sys.argv[1]   if len(sys.argv) > 1 else '2D_accurate'
    approx_directory = sys.argv[2] if len(sys.argv) > 2 else '2D_with_errors'
    field_name = sys.argv[3]       if len(sys.argv) > 3 else 'field_acceleration_x'
    max_blocks = int(sys.argv[4])  if len(sys.argv) > 4 else 5
    # ['field_acceleration_x', 'field_acceleration_y', 'field_potential_copy']

    print("started!")

    good_files = []
    for entry in os.scandir(good_directory):
        good_files.append(entry.path)

    approx_files = []
    for entry in os.scandir(approx_directory):
        approx_files.append(entry.path)

    big_numer_sum =0
    big_denom_sum =0
    for i in range(len(good_files)):
        print("{} and {}".format(good_files[i],approx_files[i]))
        [numer_sum, denom_sum] = compare_data_files(good_files[i], approx_files[i], field_name,max_blocks)
        big_numer_sum += numer_sum
        big_denom_sum += denom_sum
    print("final L2 error norm is {}".format(math.sqrt(big_numer_sum / big_denom_sum)))
