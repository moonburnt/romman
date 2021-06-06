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

# This module contains functions related to obtaining data from datasheets

import logging
from lxml import etree

log = logging.getLogger(__name__)

def dat_header_fetcher(datafile:str):
    '''Fetches group (usually name of console) and category (nointro/redump/etc)
    from provided datafile and returns them'''
    log.debug(f"Attempting to fetch header from {datafile}")
    #events expect tuple, so its like that
    raw_header = etree.iterparse(datafile, events=('end',), tag='header')

    for event, item in raw_header:
        group = item.find('name').text
        try:
            category = item.find('homepage').text
        except:
            #this tag presents in non-iso tosec dumps INSTEAD of "homepage"
            category = item.find('category').text
        #clearing up the stuff (just to be safe)
        item.clear()
        while item.getprevious() is not None:
            del item.getparent()[0]

    log.debug(f"Got following header data: {group}, {category}")

    return group, category

def roms_fetcher(datafile:str, tag:str, group:str, category:str):
    '''Returns list with games data from provided datafile'''
    log.debug(f"Attempting to info about roms from {datafile}")
    raw_roms = etree.iterparse(datafile, events=('end',), tag=tag)

    data_list = []
    for event, item in raw_roms:
        game_name = item.find('description').text
        for entry in item.findall('rom'):
            #this will reduce ram usage even further, coz we only log necessary
            #info of matching entries
            entry_data = {}
            entry_data['name'] = entry.attrib['name']
            try:
                #if I will ever decide to implement md5/sha1 verification - this
                #will need adjustments
                #applying 'lower', coz nointro has hashes in caps
                entry_data['crc'] = entry.attrib['crc'].lower()
            except KeyError:
                log.debug(
                f"{entry_data['name']} has no valid hash information. Skipping"
                )
                continue
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
        #I know how it looks, but this check is there to avoid "FutureWarning"
        while item.getprevious() is not None:
            del item.getparent()[0]

    log.debug(f"Obtained {len(data_list)} roms from {datafile}")
    return data_list

def dat_file(datafile:str):
    '''Returns list with game data from dat file.
    Only standard DAT is supported - attempting to parse other xmls will throw
    error, due to different internal structure'''
    log.debug(f"Processing datasheet: {datafile}")

    group, category = dat_header_fetcher(datafile)
    tag = "game"
    data = roms_fetcher(datafile, tag, group, category)

    log.debug(f"Successfully fetched data from {datafile}, returning")
    return data

def mame_xml(xmlfile:str):
    '''Returns list with game data from xml file.
    Only xml from zip from https://www.mamedev.org/release.php is supported'''

    log.debug(f"Processing mame xml: {xmlfile}")
    group, category = "MAME", "mamedev"
    tag = "machine"
    data = roms_fetcher(xmlfile, tag, group, category)

    log.debug(f"Successfully fetched data from {xmlfile}, returning")
    return data

