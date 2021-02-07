#this contains all the parsers to process data files
#as for now - only nointro is supported

import logging
from lxml import etree

log = logging.getLogger(__name__)

def dat_file(datafile):
    '''Receives str(path/to/datasheet.dat), returns list with games from that file (game name, files, hash sums, name of datasheet and group that made it). Only standard DAT is supported - attempting to parse other xmls will throw error, due to different internal structure'''
    log.debug(f"Processing datasheet: {datafile}")
    with open(datafile) as f:
        #going this way instead of .read() to avoid encoding-specific errors
        rawxml = etree.parse(f)

    xmldata = rawxml.getroot()

    log.debug(f"Attempting to fetch header")
    #this may fail if dat file has incorrect structure.
    #header always comes first, so we dont need to process whole xml
    for item in xmldata.getchildren()[0]:
        if item.tag == "name":
            group = item.text
        if item.tag == "category":
            category = item.text
            break #coz this tag presents in non-iso tosec dumps INSTEAD of "homepage"
        if item.tag == "homepage":
            category = item.text
            break #coz this tag goes below everything else, thus no need to parse afterwards
    log.debug(f"Got following header data: {group, category}")

    log.debug(f"Attempting to fetch game entries")
    data_list = []
    for item in xmldata.getchildren()[1:]:
        #this doesnt verify if datfile has all the necessary entries
        #meaning it will cause exception if, say, some file is but placeholder
        game_name = item.attrib['name']
        for entry in item.getchildren():
            #doing it this way coz some games may feature multiple valid files
            if entry.tag == "rom":
                #no need to specify entry_data's type coz entry.attrib is already dictionary
                entry_data = entry.attrib
                entry_data['game'] = game_name
                entry_data['group'] = group
                entry_data['category'] = category
                log.debug(f"Got following info: {entry_data}")
                data_list.append(entry_data)

    log.debug(f"Obtained {len(data_list)} entries from {datafile}")
    return data_list
