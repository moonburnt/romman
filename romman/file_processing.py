## Romman - yet another tool to compare your console ROMs with accuracy-focused datasheets
## Copyright (c) 2021 moonburnt
##
## This program is licensed under Anti-Capitalist Software License.
## For terms and conditions, see attached LICENSE file.

# This module contains functions related to working with files

import logging
from zipfile import ZipFile, is_zipfile
from os import listdir
from os.path import isfile, isdir, join, basename
from romman import hashcheck

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

def get_zip_info(pathtofile):
    '''Receives str(path/to/zipfile.zip. Return list containing dictionaries with each file's info - name, hashsum, path to archive and mention that its zip archive'''
    log.debug(f"Attempting to parse zip archive: {pathtofile}")

    datalist = []
    with ZipFile(pathtofile, 'r') as zf:
        for f in zf.infolist():
            raw_crc = f.CRC
            internal_path = f.filename
            if raw_crc == 0:
                log.debug(f'{internal_path} is directory or empty, skipping')
                continue
            else:
                data = {}
                #this is necessary coz file may be in subdirectory
                data['name'] = basename(internal_path)
                hex_crc = hex(raw_crc)
                data['crc'] = hex_crc.replace('0x', '')
                #this may be jank, but will do for log output
                #which is the only thing why this entry exists anyway
                data['path'] = join(pathtofile, internal_path)
                data['is_zip'] = True

                log.debug(f"Got following data: {data}")
                datalist.append(data)

    log.debug(f"Successfully fetched data from {pathtofile}, returning")
    return datalist

def get_file_info(pathtofile):
    '''Receives str(path/to/file). Returns list containing dictionary with filename, hashsum, path to file and mention that its not zip archive'''
    log.debug(f"Attempting to fetch info from {pathtofile}")

    #List is completely unnecessary, but since zip files have these - I kinda have to follow same route
    #I mean - its needed either there or within file processor. For now its there
    datalist = []

    crc = hashcheck.crc32sum(pathtofile)
    if crc != '0': #its str coz crc32sum always returns str
        data = {}
        data['name'] = basename(pathtofile)
        data['crc'] = crc
        data['path'] = pathtofile
        data['is_zip'] = False

        log.debug(f"Got following data: {data}")
        datalist.append(data)

    #yeah, I know. If crc == 0, returning empty list. It will be .extended to other, regardless
    log.debug(f"Successfully fetched data from {pathtofile}, returning")
    return datalist


def file_processor(pathtofile):
    '''Receives str(path/to/file). Depending on if its zip or not - fetches info from it as archive or calculates manually. Return list with dictionary containing info about filepath, file's name and crc (or, in case its archive - names and crc of all files inside), also if its zip or not'''

    log.debug(f"Determining filetype of {pathtofile}")
    if is_zipfile(pathtofile):
        log.debug(f"Seems like {pathtofile} is zip archive, proceeding accordingly")
        data = get_zip_info(pathtofile)
    else:
        log.debug(f"{pathtofile} doesnt seem to be zip, threating as file")
        data = get_file_info(pathtofile)

    log.debug(f"Successfully gathered info about {pathtofile}, returning")
    return data
