import os
import sys
from enum import Enum


class Result(Enum):
    FILE_DOES_NOT_EXIST = 1
    FILE_CONTAINS_ONLY_SEGMENT_LENGTH = 2
    LAST_LINE_CONTAINS_START_TIME_AND_SPEECH = 3
    LAST_LINE_CONTAINS_ONLY_END_TIME = 4


def read_last_line(file_path):
    with open(file_path, 'rb') as file:
        file.seek(0, 2)  # Gehe zum Ende der Datei
        if file.tell() == 0:
            return ""

        file.seek(-2, 2)  # Gehe zum zweitletzten Byte der Datei
        while file.read(1) != b'\n':
            file.seek(-2, 1)
            if file.tell() == 0:  # Datei hat nur eine Zeile ohne Zeilenumbruch
                file.seek(0)
                break

        last_line = file.readline().decode()
    return last_line.strip()


def get_end_time(file_path):
    if not os.path.isfile(file_path):
        return Result.FILE_DOES_NOT_EXIST

    last_line = read_last_line(file_path)

    if not last_line:
        return Result.FILE_CONTAINS_ONLY_SEGMENT_LENGTH

    if last_line:
        spl = last_line.split(" ")
        if len(spl) > 1:
            return ""
        else:
            return spl[0]
    else:
        return


def main():

    if len(sys.argv) != 2:
        print("missing file")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"File \"{file_path}\" does not exist.")
        exit(0)

    last_line = read_last_line(file_path)
    print("'" + last_line + "'")


if __name__ == "__main__":
    main()
