from multiprocessing import Process, Queue, Pool, cpu_count, Manager, pool
import multiprocessing
import time
from argparse import ArgumentParser
import os


# function to check whether input file exists or not
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


# function to check whether output file path exists or not
def is_valid_file_path(parser, arg):
    path = arg.split("\\")
    path = path[:-1]
    n_path = ""
    for i in path:
        n_path += i + "\\"
    if len(n_path) > 0:
        if not os.path.exists(n_path):
            parser.error("The file path %s does not exist!" % n_path)
        else:
            return open(arg, 'w')  # return an open file handle
    else:
        return open(arg, 'w')  # return an open file handle


# function to validate the no_of_processes
def no_of_process(parser, arg):
    arg = int(arg)
    if arg < 0:
        parser.error("The no_of_processes must be a positive integer greater than 0.")
    else:
        return arg


# using 'argparse' for command line argument as input, output and processes(-i. -o, -t)
parser = ArgumentParser()
# -i input file
parser.add_argument("-i", dest="filename", required=True,
                    help="input file with a matrix", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
# -o output file
parser.add_argument("-o", dest="output", required=True,
                    help="file to store generated output", metavar="FILE",
                    type=lambda x: is_valid_file_path(parser, x))
# -t no_of_process
parser.add_argument("-t", dest="processes",
                    help="number of time steps or processes", type=lambda x: no_of_process(parser, x), default=1)

args = parser.parse_args()

m = []

f = args.filename

# storing the input matrix to variable
while True:
    line = f.readline()
    if not line:
        break
    data = line.strip()
    m.append(data)


# function to find a neighbour of a cell/square
def neighbor(cell, r, c):
    x, y = cell[0], cell[1]
    return x + r, y + c


# function for finding all neighbours for the cell or square of the matrix
def find_neighbor(cell, b):
    n_cells = []
    r = [-1, 0, 1]
    for i in r:
        for j in r:
            result = neighbor(cell, i, j)
            result = list(result)
            if result[0] >= len(b):
                result[0] = 0
            elif result[0] < 0:
                result[0] = len(b) - 1

            if result[1] >= len(b[0]):
                result[1] = 0
            elif result[1] < 0:
                result[1] = len(b[0]) - 1

            result = tuple(result)
            if result != cell:
                n_cells.append(result)
    return n_cells


# this function returns the new state of the cell/square as alive or dead
def new_state(test_cell, b):
    neigh = find_neighbor(test_cell, b)
    active = []
    for i in neigh:
        r = i[0]
        c = i[1]
        active.append(b[r][c])
    n = test_cell[0]
    m = test_cell[1]
    if b[n][m] == '.':
        if active.count('O') % 2 == 0 and active.count('O') != 0:
            return True
        else:
            return False
    else:
        if active.count('O') >= 2 and active.count('O') <= 4:
            return True
        else:
            return False


def rowWise(rowNum):
    b = rowNum[1]
    rowNum = rowNum[0]
    nextRow = []

    for colNum in range(len(b[rowNum])):
        next_state = new_state((rowNum, colNum), b)
        if b[rowNum][colNum] == '.':
            if next_state:
                nextRow.append('O')
            else:
                nextRow.append('.')
        else:
            if next_state:
                nextRow.append('O')
            else:
                nextRow.append('.')
    return nextRow


# this function returns new resulting matrix for the input matrix.
def next_step(x):
    b = x

    b_next = list()
    for i in range(len(b)):
        b_next.append(list())
        for j in range(len(b[i])):
            if b[i][j] == '.':
                if new_state((i, j), b):
                    b_next[i].append('O')
                else:
                    b_next[i].append('.')
            else:
                if new_state((i, j), b):
                    b_next[i].append('O')
                else:
                    b_next[i].append('.')

    return b_next


def test_next_step(z, que):
    b = que.get()
    c = b[1]
    b = b[0]
    b_next = []
    for i in range(len(b)):
        b_next.append(list())
        for j in range(len(b[i])):
            if b[i][j] == '.':
                if new_state((i, j), b):
                    b_next[i].append('O')
                else:
                    b_next[i].append('.')
            else:
                if new_state((i, j), b):
                    b_next[i].append('O')
                else:
                    b_next[i].append('.')
    print(f'Time step #{c + 1}')
    for i in range(len(b_next)):
        for j in range(len(b_next[i])):
            print(b_next[i][j], end="")
        print(end='\n')
    print(end='\n')
    que.put((b_next, c + 1))
    return b_next



# main method
if __name__ == "__main__":
    # we use multiprocessing queue to communicate or share data between the
    # processes as they are dependent on one another's result.
    start = time.perf_counter()
    l = Manager()

    que = l.Queue()
    que.put((m, 0))
    res = []
    processPool = Pool(6)
    for _ in range(100):
        res.append(processPool.apply_async(test_next_step, (0, que)))

    finalData = []
    for i in range(len(res)):
        finalData.append(res[i].get())


    pool = Pool(args.processes)
    finals = pool.map(next_step, finalData)
    finish = time.perf_counter()


    o = args.output

    # write the resulting matrix to the output file in form of string

    final = list(finals)[-1]
    for i in range(len(final)):
        for j in range(len(final[i])):
            o.write(final[i][j])
        o.write('\n')

    print(f'Simulation complete. Final result stored in the output file "{args.output.name}"', end="\n\n")

    print(f'Finished in {round(finish - start, 5)} second(s)')

