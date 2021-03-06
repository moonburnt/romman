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

# This module contain functions related to calculating hash sums of files

from hashlib import md5
from zlib import crc32
import logging

log = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 4096

def md5sum(filepath:str, chunk_size:int = DEFAULT_CHUNK_SIZE):
    '''Calculates md5 of a file, chunk-by-chunk and returns str with sum of result'''
    log.debug(f"Processing the file {filepath}")
    #ensuring that chunk_size is not less than default
    if chunk_size < DEFAULT_CHUNK_SIZE:
        chunk_size == DEFAULT_CHUNK_SIZE
    log.debug(f"Chunk size has been set to {chunk_size}")

    hs = md5()
    #'b' coz hashsum is calculated by file's binary content
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            #this adds hashes of new chunks to previously calculated ones
            hs.update(chunk)

    hashsum = hs.hexdigest()

    log.debug(f"Got md5 sum: {hashsum}")
    return hashsum

def crc32sum(filepath:str):
    '''Calculates crc32 of a file and returns str with sum of result'''
    #TODO: add ability to calculate crc by chunks
    log.debug(f"Processing the file {filepath}")
    with open(filepath, "rb") as f:
        data = f.read()
        hs = crc32(data) & 0xffffffff

    hx = hex(hs)
    hashsum = hx.replace('0x', '')

    log.debug(f"Got crc32 sum: {hashsum}")
    return hashsum
