# This file contains functions to parse connections between two components
# The type of connection is stored as a json file  './Data/part_connectiontype.json' as a dictionary

import pandas as pd
import json
import numpy as np
from ast import literal_eval


def parse_connection():
    # TODO: Convert a connection adjacency matrix to a list, containing tuples (m, n),
    # where m is the connection type and n is the part to connect
    connectiondic = {}
    datafile = pd.ExcelFile("./data/Data.xlsx")
    # Read the data in "Connection" Sheet
    pd_connection = pd.read_excel(
        datafile, index_col=0, sheet_name="Connection")

    for column, series in pd_connection.iteritems():
        for row, v in series.items():
            if pd.notnull(v) and v != 'x' and v != 0:
                connectiondic[column] = []
                connectiondic[row] = []
                connection_methods = str(v).split(',')
                for method in connection_methods:
                    connectiondic[column].append((int(method), row))
                    connectiondic[row].append((int(method), column))

    pd_connectiondic = pd.Series(connectiondic)
    pd_connectiondic.to_csv("./data/connectionparse.csv")


def readconnections(typefile_path, connection_code):
    # read a connection tuple, return the list of 'relationships

    with open(typefile_path, 'r') as f:
        typedic = json.load(f)
    connection_type = typedic[str(connection_code)]
    return connection_type


if __name__ == '__main__':
    print(readconnections('./Data/part_connectiontype.json', 1))
