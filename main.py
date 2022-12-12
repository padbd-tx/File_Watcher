# Imports
from os import listdir
from os.path import isfile, join, getsize
import time
import datetime

# Capture configuration settings

watch_dir = r'D:\Users\Brad\Downloads'
pollTime = 5  # in seconds
log_file = 'log.txt'


# Function to return files in a directory:
def file_in_directory(my_dir: str):
    files = [(f, getsize(join(my_dir, f))) for f in listdir(my_dir) if isfile(join(my_dir, f))]

    return files


# Function comparing two lists:
def list_compare(original_list: list, new_list: list):
    sorted(original_list, key=lambda x: x[0])
    sorted(new_list, key=lambda x: x[0])

    if len(new_list) != len(original_list):
        return True
    elif original_list != new_list:
        return True
    else:
        return False


def do_things_with_new_files(new_files: list):
    print(f'File Change Detected: {new_files}')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as file:
        file.write(f'Change Record: {new_files}, {current_time} \n')


def file_watcher(my_dir: str, poll_time: int):
    while True:
        if 'watching' not in locals():
            original_list = file_in_directory(watch_dir)
            watching = 1

        time.sleep(pollTime)

        new_file_list = file_in_directory(watch_dir)

        file_diff = list_compare(original_list, new_file_list)
        differences_list = [x for x in original_list if x not in new_file_list]
        original_list = new_file_list
        if not file_diff:
            continue
        do_things_with_new_files(differences_list)


file_watcher(watch_dir, pollTime)


