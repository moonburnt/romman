## Romman - yet another tool to compare your console ROMs with accuracy-focused datasheets
## Copyright (c) 2021 moonburnt
##
## This program is licensed under Anti-Capitalist Software License.
## For terms and conditions, see attached LICENSE file.

# This module contains functions related to obtaining data from datasheets

import logging
from lxml import etree

log = logging.getLogger(__name__)

def dat_header_fetcher(datafile):
    '''Receives str(path/to/datasheet.dat), fetches group (usually name of console) and category (nointro/redump/etc). Returns str(group), str(category)'''
    log.debug(f"Attempting to fetch header from {datafile}")
    #idk why, but without "," at the end of "events" it would crash
    raw_header = etree.iterparse(datafile, events=('end',), tag='header')

    for event, item in raw_header:
        group = item.find('name').text
        try:
            category = item.find('homepage').text
        except:
            #this tag presents in non-iso tosec dumps INSTEAD of "homepage"
            category = item.find('category').text
        #clearing up the stuff (idk if it makes much difference there, but just to be safe
        item.clear()
        while item.getprevious() is not None:
            del item.getparent()[0]

    log.debug(f"Got following header data: {group}, {category}")

    return group, category

def roms_fetcher(datafile, tag, group, category):
    '''Receives str(path/to/datasheet.dat), str(tag, we will search for), str(title/name of datasheet) and str(group that made datasheet) returns list with games from that file (game name, files, hash sums, name of datasheet and group that made it)'''
    log.debug(f"Attempting to info about roms from {datafile}")
    raw_roms = etree.iterparse(datafile, events=('end',), tag=tag)

    data_list = []
    for event, item in raw_roms:
        game_name = item.find('description').text
        #I could go for separate loop, but Im lazy so Im doing another for cycle inside
        for entry in item.findall('rom'):
            #making a copy of entry.attrib dict, coz it will be wiped below
            #and yes - this saves more ram, than continuing to reference entry.attrib
            entry_data = dict(entry.attrib)
            entry_data['game'] = game_name
            entry_data['group'] = group
            entry_data['category'] = category

            log.debug(f"Got following info: {entry_data}")
            data_list.append(entry_data)
            entry.clear()
        #now cleaning up the stuff from memory, to avoid swimming in ram
        #removing the item itself
        item.clear()
        #removing all non-empty references to that item
        while item.getprevious() is not None: #I know how it looks, but this check is there to avoid "FutureWarning":
            del item.getparent()[0]

    log.debug(f"Obtained {len(data_list)} roms from {datafile}")
    return data_list

def dat_file(datafile):
    '''Receives str(path/to/datasheet.dat), returns list with games from that file (game name, files, hash sums, name of datasheet and group that made it). Only standard DAT is supported - attempting to parse other xmls will throw error, due to different internal structure'''
    log.debug(f"Processing datasheet: {datafile}")

    group, category = dat_header_fetcher(datafile)
    tag = "game"
    data = roms_fetcher(datafile, tag, group, category)

    log.debug(f"Successfully fetched data from {datafile}, returning")
    return data

def mame_xml(xmlfile):
    '''Receives str(path/to/mamedatafile.xml), returns list with games from that file (game name, files, hash sums, name of datasheet and group that made it). Only xml from zip from https://www.mamedev.org/release.php is supported'''

    log.debug(f"Processing mame xml: {xmlfile}")
    group, category = "MAME", "mamedev"
    tag = "machine"
    data = roms_fetcher(xmlfile, tag, group, category)

    log.debug(f"Successfully fetched data from {xmlfile}, returning")
    return data

