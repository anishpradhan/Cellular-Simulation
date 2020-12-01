import multiprocessing
import multiprocessing.pool
import os
import time
from argparse import ArgumentParser
from multiprocessing import Pool, Manager


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
def test_neighbor(s):
    r = s[1][0]
    c = s[1][1]
    b = s[2]
    x, y = s[0][0], s[0][1]
    del (s)
    row = x + r
    col = y + c
    del (x, r, y, c)
    if row >= len(b):
        row = 0
    elif row < 0:
        row = len(b) - 1

    if col >= len(b[0]):
        col = 0
    elif col < 0:
        col = len(b[0]) - 1
    return row, col


# function for finding all neighbours for the cell or square of the matrix
def find_neighbor(cell, b):
    r = [-1, 0, 1]

    n_cells = []
    for i in r:
        for j in r:
            result = test_neighbor((cell, (i, j), b))
            if result != cell:
                n_cells.append(result)
            else:
                continue

    return n_cells


def new_state(cell, b):
    neigh = find_neighbor(cell, b)

    active = []
    for i in neigh:
        r = i[0]
        c = i[1]
        active.append(b[r][c])
    n = cell[0]
    m = cell[1]

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


def x(rowNum):
    b = rowNum[1]
    rowNum = rowNum[0]
    nextRow = []
    colNum = [i for i in range(len(b[rowNum]))]
    for i in colNum:
        doa = new_state((rowNum, i), b)
        if b[rowNum][i] == '.':
            if doa:
                nextRow.append('O')
            else:
                nextRow.append('.')
        else:
            if doa:
                nextRow.append('O')
            else:
                nextRow.append('.')
    return nextRow


def test_step(z):
    b = queue.get()
    pool = multiprocessing.Pool(processes=args.processes)
    rowNum = [(i, b) for i in range(len(b))]
    b_next = pool.map(x, rowNum)
    print(f'Time step #{z+1}')
    for i in range(len(b_next)):
        for j in range(len(b_next[i])):
            print(b_next[i][j], end="")
        print(end='\n')
    print(end='\n')
    queue.put(b_next)
    return b_next


class NoDaemonProcess(multiprocessing.Process):

    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def f_init(q):
    global queue
    queue = q


def main(m):
    manager = multiprocessing.Manager()
    q = manager.Queue()
    q.put(m)
    p = MyPool(processes=8, initializer=f_init, initargs=[q, ])
    result = p.imap(test_step, range(100))
    p.close()
    return result


# main method
if __name__ == "__main__":
    start = time.perf_counter()
    finals = main(m)
    o = args.output
    final = list(finals)[-1]
    for i in range(len(final)):
        for j in range(len(final[i])):
            o.write(final[i][j])
        o.write('\n')

    finish = time.perf_counter()
    print(f'Simulation complete. Final result stored in the output file "{args.output.name}"', end="\n\n")
    print(f'Single process finished in {round(finish - start, 5)} second(s)')
