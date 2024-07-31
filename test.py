import os
import sys
from enum import Enum


def delete_last_line_and_append(file_path, new_content):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove the last line if the file is not empty
    if lines:
        lines = lines[:-1]

    with open(file_path, 'w') as file:
        file.writelines(lines)
        file.write(new_content + '\n')


def prepare_analysis_file(analyze_file_path):
    end_time = None
    with open(analyze_file_path, 'r') as file:
        lines = file.readlines()

    # Find the last non-empty line that is a digit and remove it
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line != "":
            end_time = int(line)
            lines = lines[:i]
            break

    return end_time, lines

def main():
    file_path = '/home/thees/tmp/test.txt'
    new_content = "This is the new content to be added."
    #delete_last_line_and_append(file_path, new_content)
    end_time, lines = prepare_analysis_file(file_path)
    print(end_time)
    print(lines)



if __name__ == "__main__":
    main()
