# Imports
import os
from os import listdir
from os.path import isfile, join, getsize
import time
import datetime
import ctypes
import win32security
from pathlib import Path

domain = os.environ['userdomain']

# Capture configuration settings

watch_dir = r"T:\CX Validations\Completed\For Production Use"
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


def get_owner(filename):
    f = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
    (username, domain, sid_name_use) = win32security.LookupAccountSid(None, f.GetSecurityDescriptorOwner())
    return username


def list_users(path_list: list):
    users_list = []
    for f in path_list:
        users_list.append(get_owner(f))
    return users_list


file_list = file_in_directory(watch_dir)
n_list = []



print(list_users(n_list))
print(len(n_list))
