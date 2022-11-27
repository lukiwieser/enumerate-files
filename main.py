from os import scandir, rename
from os.path import isfile, join, isdir


class File:
    def __init__(self, name, new_name, creation_time):
        self.name = name
        self.creation_time = creation_time
        self.new_name = new_name


class Interval:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def intersect(self, other: 'Interval') -> bool:
        if other.start > self.end or other.end < self.start:
            return False
        return True

    def intersect_number(self, other: int) -> bool:
        if other > self.end or other < self.start:
            return False
        return True


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
    print("\nStart Number of Enumeration:")
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


def input_gaps() -> list[Interval]:
    gaps: list[Interval] = []

    print("\nAdd Gaps in Enumeration. Start and End of Gap are inclusive. Finish adding gaps with [f]")
    while True:
        print("  " + str(len(gaps) + 1) + ". Gap")
        while True:
            print("    Start:")
            start_str = input("      > ")
            if start_str == "f":
                return gaps
            try:
                start = int(start_str)
            except ValueError:
                print("      Input must be a number!")
                continue
            break
        while True:
            print("    End:")
            end_str = input("      > ")
            if start_str == "f":
                return gaps
            try:
                end = int(end_str)
            except ValueError:
                print("      Input must be a number!")
                continue
            if end < start:
                print("      End cannot be smaller than Start!")
                continue
            break
        new_gap = Interval(start, end)
        intersect = False
        for gap in gaps:
            if new_gap.intersect(gap):
                print(f"     Error: New Interval intersects existing interval ({gap.start},{gap.end}).")
                intersect = True
        if intersect:
            continue

        gaps.append(new_gap)


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


def input_enumeration_seperator() -> str:
    print("\nEnumeration Seperator [e.g. __ = 001__]: ")
    enum_seperator = input("  > ")
    return enum_seperator


def add_enumeration() -> None:
    folder_path = input_folder_path()
    enum_length = input_enumeration_length()
    enum_seperator = input_enumeration_seperator()
    start_number = input_start_number()
    gaps = input_gaps()

    # get files and sort them by creation date
    files: list[File] = []
    for item in scandir(folder_path):
        if isfile(join(folder_path, item.name)):
            files.append(File(item.name, None, item.stat().st_ctime))
    files.sort(key=lambda x: x.creation_time, reverse=False)

    # determine new names of files
    print("\nNew Filenames:")
    counter = start_number
    for file in files:
        for gap in gaps:
            if gap.intersect_number(counter):
                counter = gap.end + 1

        file.new_name = str(counter).zfill(enum_length) + enum_seperator + file.name
        print(file.new_name)
        counter += 1

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
    files: list[File] = []
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
