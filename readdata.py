__author__ = 'VM_PRL'

import numpy
import csv

x = []


# reading data file
def readFile(fname):
    rows = []
    f = open(fname, 'r')
    reader = csv.reader(f, delimiter='\t')
    for n, row in enumerate(reader):
        if len(rows) < n+1:
            rows.append([])
            rows[n].extend(row)
    f.close()
    data = numpy.array(rows, float)
    return data


# reading batches of files
def readFiles(list_of_files):
    for file_name in list_of_files:
        data = readFile(file_name)
        x.append(data)
    return x


