## Romman - yet another tool to compare your console ROMs with accuracy-focused datasheets
## Copyright (c) 2021 moonburnt
##
## This program is licensed under Anti-Capitalist Software License.
## For terms and conditions, see attached LICENSE file.

# This module contain functions related to calculating hash sums of files

from hashlib import md5
from zlib import crc32
import logging

log = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 4096

def md5sum(filepath, chunk_size = DEFAULT_CHUNK_SIZE):
    '''Receives str(path to file). Optionally receives int(chunk size) (if not set or is lower than DEFAULT_CHUNK_SIZE - will fall back to it). Calculates md5 of file, chunk-by-chunk and returns str with sum of result'''
    log.debug(f"Processing the file {filepath}")
    #ensuring that chunk_size is not less than default
    if chunk_size < DEFAULT_CHUNK_SIZE:
        chunk_size == DEFAULT_CHUNK_SIZE
    log.debug(f"Chunk size has been set to {chunk_size}")

    hs = md5()
    with open(filepath, "rb") as f: #'b' coz hashsum is calculated by file's binary content
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hs.update(chunk) #this adds hashes of new chunks to previously calculated ones

    hashsum = hs.hexdigest()

    log.debug(f"Got md5 sum: {hashsum}")
    return hashsum

def crc32sum(filepath):
    '''Receives str(path to file). Calculates crc32 of file and returns str with sum of result'''
    #TODO: add ability to calculate crc by chunks
    log.debug(f"Processing the file {filepath}")
    with open(filepath, "rb") as f:
        data = f.read()
        hs = crc32(data) & 0xffffffff

    hx = hex(hs)
    hashsum = hx.replace('0x', '')

    log.debug(f"Got crc32 sum: {hashsum}")
    return hashsum
