## Romman - utility to compare your console ROMs with accuracy-focused datasheets
## Copyright (c) 2021 moonburnt
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt

# This module contains functions related to working with files

import logging
from zipfile import ZipFile, is_zipfile
from py7zr import SevenZipFile, is_7zfile
from os import listdir, makedirs
from os.path import isfile, isdir, join, basename, dirname
from romman import hashcheck

log = logging.getLogger(__name__)

def get_files(pathtodir:str):
    '''Returns list of files in directory'''
    files = []
    #this check is useless in loop below, but allows to use this function to
    #verify every item passed by user
    #maybe I should move it to separate function, but for now I wont bother
    if isfile(pathtodir):
        log.debug(f"{pathtodir} itself is a file, returning")
        files.append(pathtodir)
        return files

    log.debug(f"Attempting to parse directory {pathtodir}")
    directory_content = listdir(pathtodir)
    log.debug(f"Uncategorized content inside is: {directory_content}")

    for item in directory_content:
        log.debug(f"Processing {item}")
        itempath = join(pathtodir, item)
        if isdir(itempath):
            log.debug(f"{itempath} leads to directory, processing its content")
            #looping over this very function for all subdirectories
            files += get_files(itempath)
        else:
            #assuming that everything that isnt directory is file
            log.debug(f"{itempath} leads to file, adding to list")
            files.append(itempath)

    log.debug(f"Got following files in total: {files}")
    return files

def get_zip_info(pathtofile:str):
    '''Returns list with zip's internal files info: name, crc, path, inner filepaths'''
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
                data['crc'] = f"{raw_crc:x}"
                data['path'] = internal_path
                #unlike normal files - this one is located inside archive, so its kinda logical
                data['location'] = pathtofile
                data['is_archive'] = 'zip'

                log.debug(f"Got following data: {data}")
                datalist.append(data)

    log.debug(f"Successfully fetched data from {pathtofile}, returning")
    return datalist

def get_7z_info(pathtofile:str):
    '''Returns list with 7z's internal files info: name, crc, path, inner filepaths'''
    log.debug(f"Attempting to parse 7z archive: {pathtofile}")

    datalist = []
    with SevenZipFile(pathtofile, 'r') as sevenzf:
        for f in sevenzf.files:
            raw_crc = f.crc32
            internal_path = f.filename
            if raw_crc == 0:
                log.debug(f'{internal_path} is directory or empty, skipping')
                continue
            else:
                data = {}
                #this is necessary coz file may be in subdirectory
                data['name'] = basename(internal_path)
                data['crc'] = f"{raw_crc:x}"
                data['path'] = internal_path
                #unlike normal files - this one is located inside archive, so its kinda logical
                data['location'] = pathtofile
                data['is_archive'] = '7z'

                log.debug(f"Got following data: {data}")
                datalist.append(data)

    log.debug(f"Successfully fetched data from {pathtofile}, returning")
    return datalist

def get_file_info(pathtofile:str):
    '''Returns info about normal file: name, crc, path, name of directory'''
    log.debug(f"Attempting to fetch info from {pathtofile}")

    #List is completely unnecessary, but since zip files have these - I kinda have
    #to follow same route
    #I mean - its needed either there or within file processor. For now its there
    datalist = []

    crc = hashcheck.crc32sum(pathtofile)
    if crc != '0': #its str coz crc32sum always returns str
        data = {}
        data['name'] = basename(pathtofile)
        data['crc'] = crc
        data['path'] = pathtofile
        data['location'] = dirname(pathtofile)
        data['is_archive'] = False

        log.debug(f"Got following data: {data}")
        datalist.append(data)

    #yeah, I know. If crc == 0, returning empty list.
    #It will be .extended to other, regardless
    log.debug(f"Successfully fetched data from {pathtofile}, returning")
    return datalist

def file_processor(pathtofile:str):
    '''Depending on received file's type - fetches info from it as archive or
    calculates manually. Return list with dictionary containing info about filepath,
    file's name and crc (or, in case its archive - names and crc of all files inside),
    also if its zip or not'''

    log.debug(f"Determining filetype of {pathtofile}")
    if is_zipfile(pathtofile):
        log.debug(f"Seems like {pathtofile} is zip archive, proceeding accordingly")
        data = get_zip_info(pathtofile)
    elif is_7zfile(pathtofile):
        log.debug(f"Seems like {pathtofile} is 7z archive, proceeding accordingly")
        data = get_7z_info(pathtofile)
    else:
        log.debug(f"{pathtofile} doesnt seem to be an archive, treating as file")
        data = get_file_info(pathtofile)

    log.debug(f"Successfully gathered info about {pathtofile}, returning")
    return data

def save_file(data, filename:str, filedir:str):
    '''Saves provided binary data as filedir/filename'''
    #avoiding the situation when filedir doesnt exist
    makedirs(filedir, exist_ok=True)
    save_path = join(filedir, filename)

    #there probably should be check to ensure that you have enough disk space
    #say, by checking the size of data and comparing with free space on filedir location
    with open(save_path, 'wb') as f:
        f.write(data)

    log.debug(f"Successfully saved {filename} as {save_path}")

def extract_zip(path_to_zip:str, output_directory:str, extract_dirs:list = None):
    '''Unpacks everything (in case no valid arguments has been provided) or
    content of all selected zip's directories into provided directory'''
    log.debug(f"Attempting to unpack {path_to_zip} into {output_directory}")
    makedirs(output_directory, exist_ok=True)

    with ZipFile(path_to_zip, 'r') as zf:
        #it may be nice to check for available disk space first
        #but right now Im not doing this. Maybe later. #TODO

        #attempting to extract all files from selected directories
        #if there are no hits - just batch-extract everything
        files = None
        if extract_dirs:
            #this may backfire, if 'f' doesnt end with '/'
            #in case there are other files with names starting with 'f'
            files = {name for f in extract_dirs for name in zf.namelist() if name.startswith(f)}

        zf.extractall(output_directory, files)

    log.debug(f"Successfully extracted {path_to_zip} into {output_directory}")
