from os import scandir, rename
from os.path import isfile, join, isdir

seperator = " "


class File:
    def __init__(self, name, new_name, creation_time):
        self.name = name
        self.creation_time = creation_time
        self.new_name = new_name


def input_folder_path() -> str:
    print("\nFolder Path:")

    while True:
        path = input("  > ")
        if isdir(path):
            return path

        print("  Try again. This folder does not exist!")


def input_rename_decision() -> bool:
    print("\nDo you want to rename the files? [y] [n]")
    while True:
        decision = input("  > ")

        if decision == "y":
            return True
        if decision == "n":
            return False

        print("  Try again. Invalid input!")


def input_start_number() -> int:
    print("\nStart-Number for Enumeration:")
    while True:
        number_str = input("  > ")

        try:
            start_numer = int(number_str)
        except ValueError:
            print("  Try again. Input is not a number!")
            continue

        if start_numer < 0:
            print("  Try again. Number must be positive!")
            continue

        return start_numer


def input_char_count_remove() -> int:
    print("\nCharacter Count to remove from beginning:")
    while True:
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


def input_enumeration_length() -> int:
    print("\nLength of Enumeration [e.g. 3 = 001]: ")
    while True:
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


def add_enumeration() -> None:
    folder_path = input_folder_path()
    enum_length = input_enumeration_length()
    start_number = input_start_number()

    # get files and sort them by creation date
    files = []
    for item in scandir(folder_path):
        if isfile(join(folder_path, item.name)):
            files.append(File(item.name, None, item.stat().st_ctime))
    files.sort(key=lambda x: x.creation_time, reverse=False)

    # determine new names of files
    print("\nNew Filenames: ")
    counter = start_number
    for file in files:
        file.new_name = str(counter).zfill(enum_length) + seperator + file.name
        counter += 1
        print(file.new_name)

    # rename files (if yes)
    should_rename_files = input_rename_decision()
    if should_rename_files:
        for file in files:
            rename(join(folder_path, file.name), join(folder_path, file.new_name))

    print("\nfinished")


def remove_enumeration() -> None:
    folder_path = input_folder_path()
    chars_remove = input_char_count_remove()

    # get files
    files = []
    for item in scandir(folder_path):
        if isfile(join(folder_path, item.name)):
            files.append(File(item.name, None, item.stat().st_ctime))

    # determine new names of files
    print("\nNew Filenames: ")
    for file in files:
        file.new_name = file.name[chars_remove:]
        print(file.new_name)

    # rename files (if yes)
    should_rename_files = input_rename_decision()
    if should_rename_files:
        for file in files:
            rename(join(folder_path, file.name), join(folder_path, file.new_name))

    print("\nfinished")


def main() -> None:
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
