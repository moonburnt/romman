## Romman - yet another tool to compare your console ROMs with accuracy-focused datasheets
## Copyright (c) 2021 moonburnt
##
## This program is licensed under Anti-Capitalist Software License.
## For terms and conditions, see attached LICENSE file.

from os.path import join

# This module contains default configuration variables, to reffer to from other modules
TOOL_NAME = "romman"
PROGRAM_DIRECTORY = '.' #to be replaced with other stuff later
CACHE_DIRECTORY = join(PROGRAM_DIRECTORY, 'Cache') #maybe overkill, but for crossplatform compatibility
DEFAULT_DATASHEETS_DIRECTORY = join(PROGRAM_DIRECTORY, "Datasheets")
