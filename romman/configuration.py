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

from os.path import join

# This module contains default configuration variables, to reffer to from other modules
TOOL_NAME = "romman"
PROGRAM_DIRECTORY = '.' #to be replaced with other stuff later
CACHE_DIRECTORY = join(PROGRAM_DIRECTORY, 'Cache') #maybe overkill, but for crossplatform compatibility
DEFAULT_DATASHEETS_DIRECTORY = join(PROGRAM_DIRECTORY, "Datasheets")

NOINTRO_PREFIX = "nointro"
REDUMP_PREFIX = "redump"
TOSEC_PREFIX = "tosec"
MAME_PREFIX = "mame"
