## Generate timing statistic spreadsheets from Enzo-E gravity standard output
These two Python scripts are designed to be used on collapses running on Domain Decomposed (DD) and BiCGSTAB respectively.
They are configured to run from the Linux or Windows terminal, where the first argument is the Enzo-E output file, and the second argument is the destination CSV.  

The script works by scanning the text of the output file, collecting simulation time, wall time, and number of blocks at each cycle, and then outputting them in a table in csv format to be used creating graphs and figures.  

A set of default inputs and outputs is present in the directory to illustrate usage. 
