import sys
import os
import io
import csv
import json
from pathlib import Path


#Configure character display in Atom
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#Set CWD to script path:
os.chdir(sys.path[0])


class frequency_event:
    def __init__(self, date, name, institution, entry, exit):
        self.date = date
        self.name = name
        self.institution = institution
        self.entry = entry
        self.exit = exit


def updateData():
    def getLastIteration():
        with open(Path("_data/last_iteration.txt"), "r") as iterFile:
            last_iteration = iterFile.read()
        return last_iteration
    def setLastIteration(backup=True):
        with open(Path("_data/last_iteration.txt"), "w") as iterFile:
            last_iteration = iterFile.write(newer_iteration)
        if backup:
            with open(Path("_data/last_iteration_backup.txt"), "w") as iterFile:
                last_iteration = iterFile.write(newer_iteration)


    last_iteration = getLastIteration()
    # print("Last iteration was {}.".format(last_iteration))

updateData()
