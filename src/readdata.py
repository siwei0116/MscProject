""" This script contains a function to read data from a csv file and return a list of triple statement (as tuples)"""
import csv
import os

def read_to_triple(filename):
    fhand=open(filename)
    csvreader=csv.reader(fhand)
    next(csvreader)  #skip the first row of the csv file.
    list_of_triples=[]
    for row in csvreader:
        triple_statement=(row[0],row[1],row[2])
        list_of_triples.append(triple_statement)
    return list_of_triples

# test the function 
##cwd=os.getcwd()
#filepath=os.path.join(cwd,'data\\triple_sample1.csv')
#print(filepath)
#print(read_to_triple(filepath))