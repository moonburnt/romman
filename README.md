## Disclaimer

This is but **data verification tool**. It **does not and will never download any games**. Its designed to be used with **your very own ROM files**, you dumped from **your own consoles** (and only if your current jurisdiction legally allows that).

## Description

**Romman** (temporary name, I just didnt manage to make any nerdy joke that would fit better) is a tool to verify hashes of your console ROM files and compare them to database entries. For now it only supports No-Intro .dat files, but more to come

## Usage
- Download up-to-date .dat files from https://datomatic.no-intro.org/index.php?page=download&op=daily&s=64
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
- Compare provided files with no-intro .dat files placed into ./Datasheets
- Print total usage statistics at the end into stdout (e.g amount of hits and misses)
- Ability to specify non-default datasheet path (or directly target datasheet files) with --datfiles flag

## TODO:

- Redesign internal database structure to make process of comparing data more convenient
- Add support for redump and tosec data files (maybe also mame)
- Automatically update data files to newest available versions
- Verify games in zip archives
- Delete non-matching files or move them to separate directory (in case they are archived - move whole archives)
- Rename matching files with non-matching names (in case they are archived - skip)
- Detailed log with data about which files got affected
- Log stdout to something like info.log and stderr to error.log
- Maybe make pyqt5 gui

