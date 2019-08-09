import sys
import os
import io
import csv
import json
from pathlib import Path


# Configure character display in Atom
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# Set CWD to script path:
os.chdir(sys.path[0])


class frequency_event:
    def __init__(self, date, name, institution, entry, exit):
        self.date = date
        self.name = name
        self.institution = institution
        self.entry = entry
        self.exit = exit


def updateDataByCSV():
    """
    Main frequency data updating function.
    """
    def getLastIteration():
        # Will keep track of additions to database.
        with open(Path("_data/last_iteration.txt"), "r") as iterFile:
            last_iteration = iterFile.read()
        return last_iteration
    def setLastIteration(last_iteration, backup=True):
        # Will update number of additions to database.
        with open(Path("_data/last_iteration.txt"), "w") as iterFile:
            update_iteration = iterFile.write(str(last_iteration))
        if backup:
            with open(Path("_data/last_iteration_backup.txt"), "w") as iterFile:
                update_iteration = iterFile.write(last_iteration)
    def appendToJSON(dict_object):
        # Called to add entries to JSON on the specified format.
        # Hints from https://stackoverflow.com/questions/12994442/how-to-append-data-to-a-json-file
        with open(Path("_data/json_database.json"), "ab+") as JSONFile:
            JSONFile.seek(0,2)                                                                              #Go to the end of file
            if JSONFile.tell() == 0:                                                                        #Check if file is empty
                JSONFile.write(json.dumps([dict_object], default=lambda x: x.__dict__).encode())            #If empty, write an array
            else:
                JSONFile.seek(-1,2)
                JSONFile.truncate()                                                                         #Remove the last character, open the array
                JSONFile.write(' , '.encode())                                                              #Write the separator
                JSONFile.write(json.dumps(dict_object, default=lambda x: x.__dict__).encode())              #Dump the dictionary
                JSONFile.write(']'.encode())                                                                #Close the array
    def getCSV(last_iteration):
        # Generator for retrieving CSV data and appending to JSON.
        # Requires the last iteration as argument
        new_instances = []
        with open(Path("_testFiles/dummy_dataB.csv"), "r") as CSVFile:
            read_CSV = csv.reader(CSVFile, dialect="excel", delimiter=";")
            next(read_CSV) # Skip the header
            row_count = 1
            while row_count <= int(last_iteration):
                row_count += 1
                next(read_CSV)
            for row in read_CSV:
                print(row)
                instance_name = "row.{}".format(row_count)
                print("Instantiating '{}'".format(instance_name))
                instance_name = frequency_event(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
                # new_instances.append(instance_name)
                appendToJSON(instance_name.__dict__)
                # with open(Path("_data/json_database"), "a") as JSONFile:
                #     json.dump(instance_name.__dict__, JSONFile,
                #     indent=4, separators=(',', ': '))
                row_count += 1
        return [row_count, new_instances]


    last_iteration = getLastIteration()
    # print("Last iteration was {}.".format(last_iteration))
    updated = getCSV(last_iteration)
    # setLastIteration(updated[0], backup=False)
    # with open(Path("_data/json_database"), "a") as JSONFile:
    #     for item in updated[1]:
    #         JSONFile.write = json.dump(item.__dict__, JSONFile, indent=4)


updateDataByCSV()
for i in range(3):
    print(input("input:"))
