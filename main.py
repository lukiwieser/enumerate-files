from os import  scandir, rename
from os.path import isfile, join

my_path = "./test-files"
start_numer = 1
enumeration_length = 3
seperator = " "

class File:
    def __init__(self, name, new_name, creation_time):
        self.name = name
        self.creation_time = creation_time
        self.new_name = new_name

def inputRenameDecision() -> bool:
    print("\nDo you want to rename the files? [y] [n]")
    while (True):   
        decision = input("  > ")
        if decision == "y": 
            return True
        if decision == "n": 
            return False
        print("  Try again. Inavlid input!");

def add_enumeration():
    # get files and sort them by creation date
    files = []
    for item in scandir(my_path):
        if isfile(join(my_path, item.name)):
            files.append(File(item.name, None, item.stat().st_ctime))
    files.sort(key=lambda x: x.creation_time, reverse=False)

    # determine new names of files
    print("\nNew Filenames: ")
    counter = start_numer
    for file in files:
        file.new_name = str(counter).zfill(enumeration_length) + seperator + file.name
        counter += 1
        print(file.new_name)

    # rename files (if yes)
    should_rename_files = inputRenameDecision()
    if should_rename_files:
        for file in files:
            rename(join(my_path,file.name),join(my_path,file.new_name))

    print("\nfinished")

def remove_enumeration():
    # get files
    files = []
    for item in scandir(my_path):
        if isfile(join(my_path, item.name)):
            files.append(File(item.name, None, item.stat().st_ctime))

    # determine new names of files
    print("\nNew Filenames: ")
    for file in files:
        file.new_name = file.name[4:]
        print(file.new_name)

    # rename files (if yes)
    should_rename_files = inputRenameDecision()
    if should_rename_files:
        for file in files:
            rename(join(my_path,file.name),join(my_path,file.new_name))

    print("\nfinished")

def main():
    print("** Enumerate Files By Creation Date **\n")

    print("What do you want to do?:")
    print("  [1] Add Enumeration")
    print("  [2] Remove Enumeration")
    decision = input("  > ")

    if decision == "1":
        add_enumeration()
    elif decision == "2":
        remove_enumeration()
    else:
        print("  Error - This Selection does not exist!")

main()    