DYKWDII - Do You Know What Day It Is?
=====================================

Introduction
------------

Hello user! Thank you for using my program, inspired by the work of [Dragonexus](https://twitter.com/GDDragonexus) on Twitter <img src=https://cdn.discordapp.com/emojis/397770592050479105.gif width=25px></img>. I know it doesn't do all that much, but it was such a fantastic learning experience and I'm glad to be able to share it with you (thank you [EricVanWilderman](https://twitter.com/VanWilderman) for [your permission](./docs/EVW%20Permission%20of%20Use.png)!). Some important notes:

- **This script requires `Python 3.8` or above**, as I am addicted to [walrus operators](https://www.python.org/dev/peps/pep-0572/).
- `DYKWDII.py`, the `media` folder, and the `bin` folder must be in the same directory for this program to function.
- This program is currently only tested on Windows system is honestly unlikely to work on other platforms. Try it out if you dare though, and let me know how it goes!

Installation
------------

This program requires that certain external libraries be installed via [pip](https://pypi.org/project/pip/). This distribution comes with a `requirements.txt` file designed to streamline the process of installing these libraries. Simply navigate to the directory where `requirements.txt` is located in a terminal and run:
```
pip -r requirements.txt
```
You can then use this program in one of two ways outlined below.

Standalone Usage
----------------

This outlines the functionality of `DYKWDII.py` as a standalone meme producer!

For a full set of commands, properties and defaults, run `py DYKWDII.py -h` from the command line. Something similar (just slightly less formatted) to the following will be produced:

```
usage: DYKWDII.py [-h] [-c CAPTION] [-x WIDTH] [-y HEIGHT] [-l LOCATION] [-f FILENAME] [-e EXTENSION]

generate EricVanWilderman "Do you know what day it is?" meme clips

optional arguments:
-h, --help
    show this help message and exit

-c CAPTION, --caption CAPTION
    the caption for the meme; exceeding 34-136 characters (depending on character widths) or 3 lines guarantees encroachment
    default: "today is [today's name] [this month's name] [today's number in the month][st/nd/rd/th] [this year]"

-x WIDTH, --width WIDTH
    the width of the final exported meme; it is recommended to use dimensions corresponding to common aspect ratios
    default: 1920

-y HEIGHT, --height HEIGHT
    the height of the final exported meme; it is recommended to use dimensions corresponding to common aspect ratios
    default: 1080

-l LOCATION, --location LOCATION
    the directory where the final meme will be exported to; make sure this is a valid directory that this program has permissions to create and write to files in
    default: [directory of caller]

-f FILENAME, --filename FILENAME
    the name of the file being exported; invalid filenames will be automatically sanitized based on the current operating system
    default: "DYKWDII-OUT [[DD].[MM].[YYYY]]"

-e EXTENSION, --extension EXTENSION
    the extension of the file; must be a video format supported by FFmpeg - would recommend leaving this as default
    default: ".mp4"
```

Usage as a Utility
------------------

**Ensure that your own script is present in the same directory as `DYKWDII.py`.**

Importing the functionality of this program is as simple as:
```py
from DYKWDII import writeMeme
```

Specifiable parameters are optional and identical to the [standalone implementation](#Standalone-Usage). It is also documented below:
```py
def writeMeme(caption: Optional[Union[str, datetime]]=datetime.now(), width: Optional[int]=1920, height: Optional[int]=1080, location: Optional[str]=getcwd(), filename: Optional[str]=None, extension: Optional[str]='mp4')
```

You can also view the function documentation at any time by running the following after importing `writeMeme`:
```py
help(writeMeme)
```
