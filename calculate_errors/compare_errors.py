
import h5py
import sys
import math


def get_sum_squared_error(actual, approx) -> tuple:
    numerator = 0
    denominator = 0
    size = actual.shape
    #2D case
    if len(size) == 2:
        for i in range(size[0]):
            for j in range(size[1]):
                numerator += ((actual[i][j] - approx[i][j]) ** 2)
                denominator += (actual[i][j] ** 2)
                #or
                #numerator += ((actual[i][j] - approx[i][j]) ** 2) / (actual[i][j] ** 2)
                #denominator += 1
        return (numerator,denominator)
    # 3D case
    elif len(size) == 3:
        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    numerator += ((actual[i][j][k] - approx[i][j][k]) ** 2)
                    denominator += (actual[i][j][k] ** 2)
                    #or
                    numerator += ((actual[i][j][k] - approx[i][j][k]) ** 2) / (actual[i][j][k] ** 2)
                    denominator += 1
        return (numerator,denominator)
    else:
        assert "size of block not 2D or 3D"
# will contain tuples in form ("block name",block_error)

def is_empty_block(block):
    size = block.shape
    # 2D case
    if len(size) == 2:
        for i in range(size[0]):
            for j in range(size[1]):
                if block[i][j] != 0:
                    return False
    # 3D case
    elif len(size) == 3:
        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    if block[i][j][k] != 0:
                        return False
    else:
        assert "size of block not 2D or 3D"
    return True

def compare_data_files(file_name_true: str,file_name_approx: str, field_name: str, max_blocks = None):
    """
    takes two equivalent hdf5 data files and compares the error between the blocks.
    :param file_name_true:
    :param file_name_approx:
    :param field_name:
    :return:
    """
    with h5py.File(file_name_true, 'r') as bcg:
        with h5py.File(file_name_approx, 'r') as dd:
            block_errors = [] # will store the errors for each block as (numer/denom)

            for block_name in list(bcg.keys()):
                if (max_blocks is not None) and (len(block_errors) >= max_blocks):
                    break

                potential_bcg = bcg[block_name][field_name]
                potential_dd = dd[block_name][field_name]
                # check whether this is a completely empty (non-root) block
                if is_empty_block(potential_bcg):
                    pass
                else:
                    sum_squared_error = get_sum_squared_error(potential_bcg, potential_dd)
                    block_errors.append(sum_squared_error)
                    if len(potential_bcg.shape) == 3:
                        print("Block sample values {} to {}".format(potential_bcg[4][4][4],potential_dd[4][4][4]))
                    else:
                        print("Block sample values {} to {}".format(potential_bcg[4][4], potential_dd[4][4]))
                    #print("{} : {}".format(sum_squared_error, math.sqrt(sum_squared_error[0] / sum_squared_error[1])))
                    print("Block {} L2 error norm: {}".format(block_name,math.sqrt(sum_squared_error[0] / sum_squared_error[1])))

    numer_sum = 0
    denom_sum = 0
    for block in block_errors:
        #print("{} : {}".format(block, block[0] / block[1]))
        numer_sum += block[0]
        denom_sum += block[1]
    print("number of non-zero blocks: {}".format(len(block_errors)))
    return [numer_sum,denom_sum]



if __name__ == "__main__":
    # take optional input from system arguments
    good_file = sys.argv[1]   if len(sys.argv) > 1 else '2D_accurate/data-01-000010.h5'
    approx_file = sys.argv[2] if len(sys.argv) > 2 else '2D_with_errors/data-01-000010.h5'
    field_name = sys.argv[3]  if len(sys.argv) > 3 else 'field_potential_copy'

    # ['field_acceleration_x', 'field_acceleration_y', 'field_potential_copy']

    print("started!")
    print("{} and {}".format(good_file, approx_file))
    [numer_sum,denom_sum] = compare_data_files(good_file, approx_file, field_name)
    print("final L2 error norm is {}".format(math.sqrt(numer_sum / denom_sum)))



