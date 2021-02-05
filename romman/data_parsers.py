#this contains all the parsers to process data files
#as for now - only nointro is supported

import logging
from lxml import etree

log = logging.getLogger(__name__)

def nointro(datafile):
    '''Receives str(path/to/nointro-data-filefile.dat), returns dictionary featuring info about dat file itself and contained games (filenames, hashsums). Only standard DAT is supported - PC XML and PC XMDB will throw error, due to having different internal structure'''
    log.debug(f"Processing datasheet: {datafile}")
    with open(datafile) as f:
        rawxml = f.read()
    xmldata = etree.fromstring(rawxml)

    log.debug(f"Attempting to fetch header")
    #this may fail if dat file has incorrect structure.
    data = {} #probably need to create placeholder dictionary entries which then will be replaced with actual?
    data['filename'] = datafile
    #header always comes first, so we dont need to process whole xml
    for item in xmldata.getchildren()[0]:
        if item.tag == "name":
            data['name'] = item.text
            break #coz for now thats the only thing we need that can be gathered from header
    log.debug(f"Got following header data: {data}")

    log.debug(f"Attempting to fetch game entries")
    data_list = []
    for item in xmldata.getchildren()[1:]:
        #this doesnt verify if datfile has all the necessary entries
        #meaning it will cause exception if, say, some file is but placeholder
        datadic = {}
        datadic['game'] = item.attrib['name'] #this may backfire without try/except too
        for entry in item.getchildren():
            entry_data = [] #doing it this way coz some games may feature multiple valid files
            if entry.tag == "rom":
                entry_data.append(entry.attrib)
            datadic['files'] = entry_data
        log.debug(f"Got following game info: {datadic}")
        data_list.append(datadic)
    data['content'] = data_list

    log.debug(f"Processed content of {datafile} is the following: {data}")
    return data
