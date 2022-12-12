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
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sorted(original_list, key=lambda x: x[0])
    sorted(new_list, key=lambda x: x[0])

    if len(new_list) < len(original_list):
        rem_file = [x for x in original_list if x not in new_list]
        with open(log_file, 'a') as file:
            file.write(f'File(s) Deleted: {rem_file} at {current_time} \n')
        return rem_file
    elif len(new_list) > len(original_list):
        new_file = [x for x in new_list if x not in original_list]
        with open(log_file, 'a') as file:
            file.write(f'File(s) Added: {new_file} at {current_time} \n')
        return new_file
    else:
        return False


def do_things_with_changes(new_files: list):
    print(f'File Change Detected: {new_files}')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(new_files) == 1:
        print(f'Writing to Log.')
        with open(log_file, 'a') as file:
            file.write(f'File Change Detected: {new_files}, {current_time}\n')
    else:
        print(f'Writing to Log.')
        with open(log_file, 'a') as file:
            file.write(f'Multiple File Changes Detected: {new_files}, {current_time}\n')


def file_watcher(my_dir: str, poll_time: int):
    while True:
        if 'watching' not in locals():
            print(f'If watching block.')
            original_list = file_in_directory(watch_dir)
            print(f'Original List: {original_list}')
            watching = 1
        print(f'Sleeping start')
        time.sleep(pollTime)
        print(f'Sleeping end')
        new_file_list = file_in_directory(watch_dir)
        print(f'new_file_list: {new_file_list}')
        file_diff = list_compare(original_list, new_file_list)  # list compare returns list of files, or False
        print(f'File_Diff function return: {file_diff}')
        original_list = new_file_list
        if not file_diff:
            continue
        do_things_with_changes(file_diff)


file_watcher(watch_dir, pollTime)
