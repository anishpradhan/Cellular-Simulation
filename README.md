# Cellular-Simulation

## Cellular Simulation with Multiprocessing in Python

### Python command line to run the script:

Syntax : `python <script> -i <input_filename.txt> -o <output_filename.txt> -t <no_of_processes>`

Eg: `> python CellularSimulation.py -i time_step_0 -o output.txt -t 20`

## About this project:

This program executes the first 100 steps of a modified cellular life simulator. This simulator will receive the path to the input file as an argument containing the starting cellular matrix. The program then simulates the next 100 time-steps based on an algorithm. The simulation is guided by a handful of simplistic rules that will result in a seemingly complex simulation of cellular organisms. 

Below is an example starting cellular matrix consisting of 10 rows and 20 columns:
```
.....O..O.O....O....
...OO.....O.....O...
.......OO...O..OO...
O........OOOO...OOOO
O....OO..O..OO..OOOO
O......O....O..O...O
O.............OO...O
O..........O..O....O
.O..............O...
....O.OO.......O...O
```

### Input/Output Files
Valid input and output files should abide by the following rules:
* The matrix should only contain the following symbols:
  * Periods ‘.’ to signify currently “dead” cells.
  * Capital O’s to signify currently “alive” cells.
  * End of Line Characters marking the end of each row.
* The matrix should not contain any spaces, commas, or other delimiters between symbols.
* The matrix must separate rows with a line break.
* Files containing any other symbols beyond periods, capital O’s, and newline characters are considered
invalid.

### Processing the Matrix
Using this starting cellular matrix, the program simulates the next 100 steps of a simulation that
uses the following rules to dictate what occurs during each time step:
* Any position in the matrix with a period ‘.’ is considered “dead” during the current time step.
* Any position in the matrix with a capital ‘O’ is considered “alive” during the current time step.
* If an “alive” square has exactly two, three, or four living neighbors, then it continues to be “alive” in the
next time step.
* If a “dead” square has an even number greater than 0 living neighbors, then it will be “alive” in the next
time step.
* Every other square dies or remains dead, causing it to be “dead” in the next time step.

For this program, a neighbor is defined as any cell that touches the current cell, meaning each current cell,regardless of position, has 8 neighbor cells. Cells located at the edge should “wrap around” the matrix to find their other neighbors.  

The final matrix (Time Step 100) after simulating step 1 through 100 will then be written to an output file whose name and path is dictated by a separate command line argument. These files contains a copy of the matrix matrix with each row of the matrix printed on separate lines and no characters in between the columns.

### Multiprocessing

This program makes use of multiprocessing and spawns a total number of processes equivalent to the number specified by the user in the -t option.

