# Romman

## Disclaimer

This is but **data verification tool**. It **does not and will never download any games**. Its designed to be used with **your very own ROM files**, you dumped from **your own consoles** (and only if your current jurisdiction legally allows that).

## Description

**Romman** (short of "rom manager". I dont like it too, if you can find a better name - make an issue) is a tool to verify hashes of your console ROM files and compare them with entries from datasheets, considered "the most accurate" by community (meaning if your rom didnt match any of these - then you probably dumped it incorrectly). Right now the following datasheet sources are supported: no-intro, tosec, redump.

## Usage
- Download up-to-date .dat files from your source of choice (supported providers listed in description above)
- Unpack them to ./Datasheets
- Run `./romman-cli files-you-want-to-verify`

Example usage:
`./romman-cli myfancyrom.gba`

Example output will be like:
`Romman has finished its job: got 1 files matching provided database and 0 misses`

You can also parse content of whole directories. Say, to fetch everything inside (including content of all subdirectories) of "Mydir", just type:
`./romman-cli ./Mydir`

For complete list of currently available functionality run
`./romman-cli -h`

## Currently implemented:
- Compare roms with no-intro/tosec/redump .dat files (either placed into ./Datasheets directory or specified with --datfiles flag)
- Log info about which ROM has matched which entry from which datasheet
- Print total usage statistics at the end (e.g amount of hits, misses and files tool couldnt verify for whatever reasons) into stdout

## TODO:

- Maybe add support for mame xmls
- Ability to fetch newest available datasheets
- Verify games in zip archives
- Delete non-matching files or move them to separate directory (in case they are archived - move whole archives)
- Rename matching files with non-matching names (in case they are archived - skip)
- Avoid swimming in ram (either by dumping data into cache file or comparing files directly with sheets, without keeping them in ram)
- Log stdout to something like info.log and stderr to error.log
- Maybe make pyqt5 gui
- Find a better name

## License:

For memes, [ACSL v1.4](LICENSE)
