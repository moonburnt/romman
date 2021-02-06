# Stuff related to processing files. Get list of them, rename, move, remove
import logging

from os import listdir
from os.path import isfile, isdir, join

log = logging.getLogger(__name__)

def get_files(dirname):
    '''Receives str(path to directory with files), returns list(files in directory)'''
    files = []
    #this check is useless in loop below, but allows to use this function to verify every item passed by user
    #maybe I should move it to separate function, but for now I wont bother
    if isfile(dirname):
        log.debug(f"{dirname} itself is a file, returning")
        files.append(dirname)
        return files

    log.debug(f"Attempting to parse directory {dirname}")
    directory_content = listdir(dirname)
    log.debug(f"Uncategorized content inside is: {directory_content}")

    for item in directory_content:
        log.debug(f"Processing {item}")
        itempath = join(dirname, item)
        if isdir(itempath):
            log.debug(f"{itempath} leads to directory, attempting to process its content")
            files += get_files(itempath) #looping over this very function for all subdirectories
        else:
            #assuming that everything that isnt directory is file
            log.debug(f"{itempath} leads to file, adding to list")
            files.append(itempath)

    log.debug(f"Got following files in total: {files}")
    return files
