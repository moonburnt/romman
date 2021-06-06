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

# This module contains functions related to updating datasheets to their newest versions

import logging
import requests
from re import findall
from time import sleep
from os import remove
from os.path import join
from romman import file_processing, configuration
log = logging.getLogger(__name__)

CACHE_DIRECTORY = configuration.CACHE_DIRECTORY
DEFAULT_DATASHEETS_DIRECTORY = configuration.DEFAULT_DATASHEETS_DIRECTORY
DATASHEETS_DOWNLOAD_DIRECTORY = join(CACHE_DIRECTORY, 'Downloads')

NOINTRO_PREFIX = configuration.NOINTRO_PREFIX
REDUMP_PREFIX = configuration.REDUMP_PREFIX
TOSEC_PREFIX = configuration.TOSEC_PREFIX
MAME_PREFIX = configuration.MAME_PREFIX

NOINTRO_URL = 'https://datomatic.no-intro.org'
TOSEC_URL = 'https://www.tosecdev.org'
REDUMP_URL = 'http://redump.org' #yep, is http coz redump has no https version
MAME_URL = 'https://www.mamedev.org'
SESSION = requests.Session()
SESSION.timeout = 100

log = logging.getLogger(__name__)

def get_nointro():
    '''Downloads daily nointro dat pack in zip.
    Saves into DATASHEETS_DOWNLOAD_DIRECTORY/NOINTRO_PREFIX'''
    url = f'{NOINTRO_URL}/index.php?page=download&op=daily&s=64'
    log.debug(f"Attempting to download latest nointro datasheets from {url}")
    get_download_link = SESSION.post(url,
                                     headers={'referer': url},
                                     data={
                                           'dat_type': 'standard',
                                           'daily_download': 'Prepare',
                                           'recaptcha_response': "",
                                           },
                                    )
    download_link = get_download_link.url
    log.debug(f"Got download link: {download_link}. "
               "Trying to fetch archive (may take a while)")
    datasheet_archive = SESSION.post(download_link,
                                     headers={'referer': download_link},
                                     data={
                                            'wtwtwtf': 'Download',
                                            'what_im_doing_here': "",
                                            },
                                    )
    log.debug(f"Successfully retrieved datasheets archive, attempting to save")
    download_directory = join(DATASHEETS_DOWNLOAD_DIRECTORY, NOINTRO_PREFIX)
    file_processing.save_file(data = datasheet_archive.content,
                              filename = 'nointro.zip',
                              filedir = download_directory)

def get_tosec():
    '''Downloads latest available tosec dat pack in zip.
    Saves into DATASHEETS_DOWNLOAD_DIRECTORY/TOSEC_PREFIX'''
    url = f'{TOSEC_URL}/downloads'
    log.debug(f"Attempting to download latest tosec datasheets from {url}")
    get_downloads = SESSION.get(url)
    dpu = findall('<div class="pd-subcategory"><a href="(.*)">', get_downloads.text)
    download_page_url = f"{TOSEC_URL}{dpu[0]}"
    log.debug(f"Got downloads page url: {download_page_url} fetching")
    download_page = SESSION.get(download_page_url)
    dps = findall('<a class="" href="(.*?)"', download_page.text)
    download_link = f"{TOSEC_URL}{dps[0]}"
    log.debug(f"Got downloads link: {download_link}. "
               "Trying to fetch archive (may take a while)")
    datasheet_archive = SESSION.get(download_link)
    log.debug(f"Successfully retrieved datasheets archive, attempting to save")
    download_directory = join(DATASHEETS_DOWNLOAD_DIRECTORY, TOSEC_PREFIX)
    file_processing.save_file(data = datasheet_archive.content,
                              filename = 'tosec.zip',
                              filedir = download_directory)

def get_redump():
    '''Downloads latest available redump dat packs in zip.
    Saves into DATASHEETS_DOWNLOAD_DIRECTORY/REDUMP_PREFIX'''
    url = f'{REDUMP_URL}/downloads'
    log.debug(f"Attempting to download latest redump datasheets from {url}")
    get_downloads = SESSION.get(url)
    raw_dl = findall('<a href="/datfile/(.*?)/">', get_downloads.text)
    #removing bios dats, coz they are broken and impossible to unpack
    dl = [item for item in raw_dl if not item.endswith('-bios')]
    log.debug(f"Got following entries to fetch: {dl}")

    for item in dl:
        download_link = f'{REDUMP_URL}/datfile/{item}/'
        filename = f'redump-{item}.zip'
        log.debug(f"Got downloads link: {download_link}. "
                   "Trying to fetch archive (may take a while)")
        datasheet_archive = SESSION.get(download_link)
        log.debug(f"Successfully retrieved datasheets archive, attempting to save")
        download_directory = join(DATASHEETS_DOWNLOAD_DIRECTORY, REDUMP_PREFIX)
        file_processing.save_file(data = datasheet_archive.content,
                                  filename = filename,
                                  filedir = download_directory)
        sleep(3) #smol pause to avoid getting banned for loads of requests

def get_mame():
    '''Downloads latest available mame dat pack in zip.
    Saves into DATASHEETS_DOWNLOAD_DIRECTORY/MAME_PREFIX'''
    url = f'{MAME_URL}/release.php'
    log.debug(f"Attempting to download latest mame datasheet from {url}")
    get_downloads = SESSION.get(url)
    dl = findall('<a href="(.*?).zip">', get_downloads.text)
    download_link = f"{dl[0]}.zip"
    log.debug(f"Got downloads link: {download_link}. "
               "Trying to fetch archive (may take a while)")
    datasheet_archive = SESSION.get(download_link)
    log.debug(f"Successfully retrieved datasheets archive, attempting to save")
    download_directory = join(DATASHEETS_DOWNLOAD_DIRECTORY, MAME_PREFIX)
    file_processing.save_file(data = datasheet_archive.content,
                              filename = 'mame.zip',
                              filedir = download_directory)

def datasheets_updater(sources:list):
    '''Match received sources against known prefixes, then for all matches -
    download related latest datasheets and unpack them into their subdirectories
    inside DEFAULT_DATASHEETS_DIRECTORY. If no valid arguments has been provided
    - will batch-download all datasheets'''
    log.debug('Determining the list of download sources')
    #using sets to avoid situations when user supplied multiple arguments of same value
    #could only do that for non-default thing, but I want consistency
    default_prefixes = {NOINTRO_PREFIX, REDUMP_PREFIX, TOSEC_PREFIX, MAME_PREFIX}
    prefixes = {item for item in sources for prefix in default_prefixes if item == prefix}

    if not prefixes:
        prefixes = default_prefixes

    log.debug(f'Got following prefixes: {prefixes}')
    for prefix in prefixes:
        if prefix == NOINTRO_PREFIX:
            downloader = get_nointro
        elif prefix == REDUMP_PREFIX:
            downloader = get_redump
        elif prefix == TOSEC_PREFIX:
            downloader = get_tosec
        elif prefix == MAME_PREFIX:
            downloader = get_mame
        else:
            #it should NOT be possible to trigger this, Im just trying to be extra cautious
            log.warning(f"Unknown prefix: {prefix}. Skipping")
            continue

        log.debug(f'Attempting to download latest datasheets from {prefix}')
        try:
            downloader()
        except Exception as e:
            log.warning(f"Unable to fetch latest datasheet: {e}. Skipping")
            continue

        log.debug(f"Getting the list of downloaded archives")
        archive_directory = join(DATASHEETS_DOWNLOAD_DIRECTORY, prefix)
        archives = file_processing.get_files(archive_directory)
        if not archives:
            log.debug(f"{archive_directory} contains no archives! Skipping")
            continue

        datasheets_directory = join(DEFAULT_DATASHEETS_DIRECTORY, prefix)
        log.debug(f"Removing old datasheets from {datasheets_directory}")
        #hopefully our user dont store anything of value inside datasheets_directory
        old_datasheets = file_processing.get_files(datasheets_directory)
        for f in old_datasheets:
            try:
                log.debug(f"Removing {f}")
                remove(f)
            except Exception as e:
                log.warning(f"Unable to remove {f}: {e}. Skipping")
                continue

        log.debug(
        f"Extracting datasheets from {archive_directory} to {datasheets_directory}"
        )
        for ar in archives:
            #avoiding tosec-specific issue with archives containing non-dat garbage
            if prefix == TOSEC_PREFIX:
                fetch_dirs = ['TOSEC/', 'TOSEC-ISO/']
                extractor_args = ar, datasheets_directory, fetch_dirs
            else:
                extractor_args = ar, datasheets_directory

            try:
                file_processing.extract_zip(*extractor_args)
            except Exception as e:
                log.warning(
                f"Unable to extract {ar} into {datasheets_directory}: {e}. Skipping"
                )
                continue
            else:
                log.debug(f"Removing {ar} from cache")
                remove(ar)
