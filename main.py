from os import  scandir, rename
from os.path import isfile, join

my_path = "./test-files"
start_numer = 1
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

def input_char_count_remove():
    print("\nCharater Count to remove from beginning:")
    while (True):   
        char_count_str = input("  > ")

        try:
            char_count = int(char_count_str)
        except ValueError:
            print("  Try again. Input is not a number!")
            continue

        if char_count < 1 or char_count > 20:
            print("  Try again. Length must be between 1 and 20!")
            continue

        return char_count

def input_enumeration_length():
    print("\nLength of Enumeration [e.g. 3 = 001]: ");
    while (True):   
        enum_length_str = input("  > ")

        try:
            enum_length = int(enum_length_str)
        except ValueError:
            print("  Try again. Input is not a number!")
            continue

        if enum_length < 1 or enum_length > 20:
            print("  Try again. Length must be between 1 and 20!")
            continue

        return enum_length

def add_enumeration():
    enum_length = input_enumeration_length()

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
        file.new_name = str(counter).zfill(enum_length) + seperator + file.name
        counter += 1
        print(file.new_name)

    # rename files (if yes)
    should_rename_files = inputRenameDecision()
    if should_rename_files:
        for file in files:
            rename(join(my_path,file.name),join(my_path,file.new_name))

    print("\nfinished")

def remove_enumeration():
    chars_remove = input_char_count_remove()

    # get files
    files = []
    for item in scandir(my_path):
        if isfile(join(my_path, item.name)):
            files.append(File(item.name, None, item.stat().st_ctime))

    # determine new names of files
    print("\nNew Filenames: ")
    for file in files:
        file.new_name = file.name[chars_remove:]
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