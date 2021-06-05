# Romman

## Disclaimer

This is but **data verification tool**. It **does not and will never download any games**. Its designed to be used with **your very own ROM files**, you dumped from **your own consoles** (and only if your current jurisdiction legally allows that).

## Description

**Romman** (short of "rom manager". I dont like it too, if you can find a better name - make an issue) is a tool to verify hashes of your console ROM files and compare them with entries from datasheets, considered "the most accurate" by community (meaning if your ROM didnt match any of these - then you probably dumped it incorrectly). Right now the following datasheet sources are supported: no-intro (only "Standard DAT"), tosec, redump, mame (only large xml from site, not separate data files from github).

## Dependencies
- python 3.8 (may work on older versions, didnt test)
- requests (to fetch newest datasheets)

## Usage
- `./romman-cli --update datfiles`, to automatically download latest available datasheets
- `./romman-cli files-you-want-to-verify`, to verify your ROMs against these

Say, you want to verify 'myfancyrom.gba' and 'anotherrom.nds', located somewhere inside './Roms' directory. Just do:
`./romman-cli ./Roms`

After comparing your files with available datasheets (may take a while, if there are many), you will get something like that:
![Example output](https://i.fiery.me/QMOXB.png?raw=true)

For complete list of currently available functionality, run:
`./romman-cli -h`

## Currently implemented:
- Compare ROMs with no-intro/tosec/redump .dat files or mame .xml (either placed into ./Datasheets directory or specified with --datfiles flag)
- Log info about which ROM has matched which entry from which datasheet
- Print total usage statistics at the end (e.g amount of hits, misses and files tool couldnt verify for whatever reasons) into stdout
- Iterative datasheets parsing, so 250mbytes-large file wont eat all your ram
- Ability to verify ROMs stored inside zip archives
- `--update-datfiles` flag to download latest available datasheets. Can be used with provider-specific prefixes. If no valid (or no prefixes at all) has been received - will batch-download datasheets from all supported providers. You can get list of valid prefixes by running `romman-cli -h`
- Notify user if some file with correct hashsum has incorrect filename.
- `--allow-rename` flag that enables ability to rename files with correct hashsums, but incorrect names. For as long as these arent part of archive

## TODO:

- Flag to delete files with incorrect hashsums (in case they are archived - skip)
- Flag to move files with incorrect hashsums into provided directory (in case they are archived - skip)
- Maybe something like `--affect-archives` flag, to enable ability to rename/remove archived files the same way as unarchived, if related action flags has been provided
- Maybe add ability to verify files by other means than crc32 (e.g md5 or sha1 or just filesize. In case of first two - archives will be skipped, obviously)
- Maybe log stdout to something like info.log and stderr to error.log
- Maybe reduce ram usage even further (probably by providing hard limits on maximum database size and dumping it into cache file, if it gets to that point)
- Maybe add ability to verify 7z-archived ROMs
- Maybe make pyqt5 gui
- Find a better name

## License:

[GPLv3](LICENSE)
