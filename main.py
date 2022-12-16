# Imports
from os import listdir
from os.path import isfile, join, getsize
import time
import datetime
import tkinter as tk
from tkinter import messagebox as msgb

# Capture configuration settings
watch_dir = r'T:\CX Validations\Completed'
pollTime = 5  # in seconds
log_file = 'log.txt'


# Function to return files in a directory:
def file_in_directory(my_dir: str):
    """
    This function takes a directory path as input and returns a list of files in the directory, along with their sizes.

    :param my_dir: The directory path to search for files.
    :box_type my_dir: str
    :return: A list of tuples containing the file names and sizes.
    :rtype: list
    """
    files = [(f, getsize(join(my_dir, f))) for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return files


# Define a message box:
def show_message(message, box_type='info', timeout=2500):
    """
    show_message(message, box_type='info', timeout=2500)

    Displays a message box with the given message, box_type, and timeout.

    Args:
    message (str): The message to be displayed in the message box.
    box_type (str, optional): The box_type of message to be displayed. Can be 'info', 'warning', or 'error'.
    Defaults to 'info'.
    timeout (int, optional): The time in milliseconds after which the message box will be automatically closed.
        Defaults to 2500.

    Returns:
    None
    """
    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if box_type == 'info':
            msgb.showinfo('Change Detected', message, master=root)
        elif box_type == 'warning':
            msgb.showwarning('Warning', message, master=root)
        elif box_type == 'error':
            msgb.showerror('Error', message, master=root)
    except (tk.TclError, ValueError):
        pass


# Function comparing two lists:
def list_compare(original_list: list, new_list: list):
    """
    This function compares two lists of files and returns a list of files that are present in the second list but not
    in the first, or False if there are no differences between the lists.

    :param original_list: The first list of files to compare.
    :box_type original_list: List[Tuple[str, int]]
    :param new_list: The second list of files to compare.
    :box_type new_list: List[Tuple[str, int]]
    :return: A list of files that are present in the second list but not in the first,
     or False if there are no differences between the lists.
    :rtype: Union[List[Tuple[str, int]], bool]
    """
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sorted(original_list, key=lambda x: x[0])
    sorted(new_list, key=lambda x: x[0])

    if len(new_list) < len(original_list):
        rem_file = [x for x in original_list if x not in new_list]
        with open(log_file, 'a') as file:
            file.write(f'\nFile(s) Deleted: {rem_file} at {current_time} \n')
        return rem_file
    elif len(new_list) > len(original_list):
        new_file = [x for x in new_list if x not in original_list]
        with open(log_file, 'a') as file:
            file.write(f'\nFile(s) Added: {new_file} at {current_time} \n')
        return new_file
    else:
        return False


def do_things_with_changes(new_files: list):
    """
    This function takes in a list of files and prints a message indicating the number of files that have changed.
    If there is only one file that has changed, it logs the details of the change along with the current time
     to a log file. If there are multiple files that have changed, it logs a message indicating that multiple files
      have changed, along with the details of the changes and the current time.

    :param new_files:
    """
    print(f'File Change Detected: {new_files}')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    show_message(f'A change has been detected in {watch_dir}\n'
                 f'The change happened at {current_time}.\n'
                 f'\nCheck the log file for details.', box_type='info', timeout=10000)
    if len(new_files) == 1:
        with open(log_file, 'a') as file:
            file.write(f'File Change Detected: {new_files}, {current_time}\n')
    else:
        with open(log_file, 'a') as file:
            file.write(f'Multiple File Changes Detected: {new_files}, {current_time}\n')


def file_watcher(my_dir: str, poll_time: int):
    """
    This function takes in a directory and a poll time, and continually checks the directory for changes.
    When changes are detected, it logs the details of the changes along with the current time to a log file.

    :param my_dir:
    :param poll_time:
    :return:
    """
    while True:
        if 'watching' not in locals():
            original_list = file_in_directory(watch_dir)
            watching = 1
            print(f'Watching: {watch_dir}')
        time.sleep(pollTime)
        new_file_list = file_in_directory(watch_dir)
        file_diff = list_compare(original_list, new_file_list)  # list compare returns list of files, or False
        original_list = new_file_list
        if not file_diff:
            continue
        do_things_with_changes(file_diff)


file_watcher(watch_dir, pollTime)
