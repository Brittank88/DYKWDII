"""
Author: Brittank88
Credits:
    - ImageMagick Studio LLC for their ImageMagick software.
    - FFmpeg Project for their FFmpeg software.
    - patorjk for his text to ASCII art generator (I'm using the fitted Cybermedium font here).
"""

# .--.      .--.      .--.      .--.      .--.      .--.    | _ _  ____ _______________ | .--.      .--.      .--.      .--.      .--.      .--.#
#::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::| | |\/||__]|  ||__/ | [__  |:::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.#
#      `--'      `--'      `--'      `--'      `--'     `-| | |  ||   |__||  \ | ___] |-'      `--'      `--'      `--'      `--'      `--'     #

# Type Hints
from __future__ import annotations
from typing import Tuple, List, Optional, Union, NoReturn

# Logging
from logging import debug, info, warn

# Filepath
from os.path import abspath, join
from pathvalidate import sanitize_filepath, sanitize_filename

# Python version check.
from sys import version_info

# Setting up ImageMagick env path for moviepy to use.
from moviepy.config import get_setting, change_settings
from os import getcwd, name as OSNAME
from subprocess import PIPE, DEVNULL, Popen

# Video creation.
# MoviePy is imported following ImageMagick configuration.
from datetime import datetime

# .--.      .--.      .--.      .--.      .--.      .--| ___ _____________  __  _______ |--.      .--.      .--.      .--.      .--.      .--.  #
#::::.\::::::::.\::::::::.\::::::::.\::::::::.\:::::::| |  \|___|___|__||  ||   | [__  |:::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\:#
#      `--'      `--'      `--'      `--'      `--'  | |__/|___|   |  ||__||___| ___] |      `--'      `--'      `--'      `--'      `--'      `#

# Internal properties that control how the separate clips join together to form the final meme.
# These should never have to be modified.
__lenC1        : float = 1.566
__lenC2        : float = 4.466
__lenCrossfade : float = 0.1

# Caption dimension boundaries.
__CAPTION_WIDTH_WARN  : int = 34
__CAPTION_WIDTH_MAX   : int = 136
__CAPTION_HEIGHT_WARN : int = 2
__CAPTION_HEIGHT_MAX  : int = 3

# Asset paths.
__MUSIC_PATH : str = './media/audio/SND.aac'
__VIDEO_PATH : str = './media/video/P1.mp4'
__MEME_PATH  : str = './media/image/P2.jpg'
__FONT_NAME  : str = 'Times-New-Roman'

# Export filename 'template' for strftime.
__NAME_FORMAT = 'DYKWDII-OUT [%d.%m.%Y]'

#  .--.      .--.      .--.      .-| _ _  ______________  _______________  _   _____  __________  ___  _____ |-.     .--.      .--.      .--.   #
#:::::.\::::::::.\::::::::.\::::::| | |\/||__|| __|___|\/||__|| __||   |_/    |   |__||___|   |_/ ||\ || __ |:.\::::::::.\::::::::.\::::::::.\::#
#'      `--'      `--'      `--' | | |  ||  ||__]|___|  ||  ||__]||___| \_   |___|  ||___|___| \_|| \||__] |    `--'      `--'      `--'      `-#

"""
Here, we check to make sure the ImageMagick binary required by MoviePy for TextClips is present and has the proper IMAGEMAGICK_BINARY env set.

MoviePy's default_conf.py checks the IMAGEMAGICK_BINARY env to see if it has been set, and uses that if so.
"""

# Attempt to execute ImageMagick on the path present in the env.
info('Configuring ImageMagick install...')
debug(f'Testing for existing ImageMagick installation on \'{OSNAME}\' OS...')
try:
    Popen(
        get_setting(__IMENV := 'IMAGEMAGICK_BINARY'),
        **{
            'stdout'        : sp.PIPE,
            'stderr'        : sp.PIPE,
            'stdin'         : DEVNULL,
            'creationflags' : 0x08000000 if OSNAME == 'nt' else None
        }
    ).communicate()
except: # If executing on the existing path didn't work, update the moviepy setting.
    debug(f'ImageMagick path was invalid or does not exist. Setting {__IMENV} parameter of MoviePy to local installation...')
    change_settings({__IMENV : abspath('./bin/imagemagick/magick.exe')})
# Placing editor import in the finally block so it is only imported after the ImageMagick path has been set up.
finally:
    info('ImageMagick configuration complete!')
    import moviepy.editor as MPE

# .--.      .--.      .--.      .--.      .--.      .-| _____  __  ______________  _____ |-.      .--.      .--.      .--.      .--.      .--.  #
#::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::| |___|  ||\ ||    | ||  ||\ |[__  |::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\:#
#      `--'      `--'      `--'      `--'      `--' | |   |__|| \||___ | ||__|| \|___] |     `--'      `--'      `--'      `--'      `--'      `#

"""
Contains the main and utility functions of this file.
"""

#    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# [=== === === === === === === === === ===] UTIL [=== === === === === === === === === ===]
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`

def __checkPyVersion() -> Union[NoneType, NoReturn]:
    """Ensures that the python version running the script is 3.8 or higher."""

    if version_info < (3, 8): raise RuntimeError(f'Python {version_info.major}.{version_info.minor}.{version_info.micro} < Python 3.8; script cannot function.')

def __captionFromDate(dateObj: Optional[datetime] = datetime.now()) -> str:
    """Generates a default caption using the date provided by dateObj."""

    # Get date components as strings.
    dName, mName, dNum, yNum = dateObj.strftime('%A|%B|%#d|%Y').split('|')

    return f'Today is {dName} {mName} {dNum}{({1: "st", 2: "nd", 3: "rd"}).get(dNum, "th")} {yNum}'.lower()

#    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
# [=== === === === === === === === === ===] MAIN [=== === === === === === === === === ===]
#`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`

def writeMeme(
    caption    : Optional[Union[str, datetime]] = datetime.now(),
    width      : Optional[int]                  = 1920,
    height     : Optional[int]                  = 1080,
    location   : Optional[str]                  = getcwd(),
    filename   : Optional[str]                  = None,
    extension  : Optional[str]                  = 'mp4'
) -> str:
    """Generates and returns a single "Do you know what day it is?" meme clip."""

    # Double-check the Python version.
    __checkPyVersion()

    # Handle filename default.
    if isinstance(caption, datetime) and not filename: filename = caption.strftime(__NAME_FORMAT)
    elif not filename: filename = datetime.now().strftime(__NAME_FORMAT)

    # Provide caption warnings only if a custom caption is being used.
    if not (captionIsDate := isinstance(caption, datetime)):

        # Warn user if their caption is too tall and may overlap video elements.
        debug('Checking caption height...')
        if c := caption.count('\n') > __CAPTION_HEIGHT_WARN: warn(f'{c} lines high caption may encroach video elements!')
        elif c > __CAPTION_HEIGHT_MAX: warn(f'{c} lines high caption will definitely overlap video elements!')

        debug('Checking caption width...')
        # Warn the user if some of their caption lines could be cut off horizontally in the video.
        for pos, line in enumerate(caption.split('\n')):
            if l := len(line) > __CAPTION_WIDTH_WARN: warn(f'Line {pos} will definitely exit sides of video frame!')
            elif l > __CAPTION_WIDTH_MAX: warn(f'Line {pos} may exit sides of video frame!')
    
    info('Beginning video construction...')
    debug('Creating meme music AudioFileClip...')
    with (  # Audio clip for caption clip.
        MPE.AudioFileClip(__MUSIC_PATH, fps=48000)
        .set_duration(__lenC2)
        .set_start(startC2 := __lenC1 - __lenCrossfade)
    ) as CFinalAudio:
        
        debug('Importing original EVW video to VideoFileClip...')
        with (  # Original EVW Clip
            MPE.VideoFileClip(__VIDEO_PATH)
            .set_duration(__lenC1)
            .fadein(__lenC1)
        ) as C1:
            
            debug('Importing caption meme to ImageClip...')
            with (  # Caption clip image.
                MPE.ImageClip(__MEME_PATH)
                .set_position(('center', 'center'))
                .set_duration(__lenC2)
                .set_start(startC2)
                .crossfadein(__lenCrossfade)
                .set_audio(CFinalAudio)
            ) as C2:
                
                debug('Creating TextClip from caption...')
                with (  # Caption clip text: "Today is <Day Name> <Month Name> <Day Number> <Year>".
                    MPE.TextClip(
                        txt      = __captionFromDate(caption) if captionIsDate else caption,
                        font     = __FONT_NAME,
                        fontsize = 62,
                        color    = 'white'
                    )
                    .margin(bottom = 45, opacity = 0)
                    .set_position(('center','bottom'))
                    .set_duration(__lenC2)
                    .set_start(startC2)
                    .crossfadein(__lenCrossfade)
                ) as C2Txt:

                    debug('Compositing and resizing final meme...')
                    with MPE.CompositeVideoClip([C1, C2, C2Txt]).resize((width, height)) as CFinal:

                        # Hacky fix for CompositeAudioClip missing fps property bug.
                        debug('Configuring audio FPS...')
                        CFinal.audio = CFinal.audio.set_fps(CFinalAudio.fps)

                        # Return the CompositeVideoClip instance.
                        CFinal.write_videofile(out := sanitize_filepath(abspath(join(location, f'{filename}.{extension.split(".")[-1]}')), platform = 'auto'), audio_codec = 'aac')
                        info('Meme created!')

    # Return the path to the exported video.
    return out

#  .--.      .--.      .--.      .--.      .--.      .--.   | ___ ______  _________ |  .--.      .--.      .--.      .--.      .--.      .--.   #
#:::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\:| |  \|__/||  ||___|__/ |::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::#
#'      `--'      `--'      `--'      `--'      `--'      | |__/|  \| \/ |___|  \ |`--      `--'      `--'      `--'      `--'      `--'      `-#

if __name__ == '__main__':

    # Double-check the Python version.
    __checkPyVersion()

    # Import our argument parser.
    from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS

    # Instantiate our argument parser.
    parser = ArgumentParser(
        description     = 'generate EricVanWilderman "Do you know what day it is?" meme clips',
        argument_default= SUPPRESS,
        formatter_class = RawTextHelpFormatter
    )

    # Add valid arguments for writeMeme().
    parser.add_argument('-c', '--caption', type = str, help = (
        'the caption for the meme; exceeding 34-136 characters (depending on character widths) or 3 lines guarantees encroachment\n'
        'default: "today is [today\'s name] [this month\'s name] [today\'s number in the month][st/nd/rd/th] [this year]"'
    ))
    parser.add_argument('-x', '--width', type = int, help = (
        'the width of the final exported meme; it is recommended to use dimensions corresponding to common aspect ratios\n'
        'default: 1920'
    ))
    parser.add_argument('-y', '--height', type = int, help = (
        'the height of the final exported meme; it is recommended to use dimensions corresponding to common aspect ratios\n'
        'default: 1080'
    ))
    parser.add_argument('-l', '--location', type = str, help = (
        'the directory where the final meme will be exported to; make sure this is a valid directory that this program has permissions to create and write to files in\n'
        'default: [directory of caller]'
    ))
    parser.add_argument('-f', '--filename', type = str, help = (
        'the name of the file being exported; invalid filenames will be automatically sanitized based on the current operating system\n'
        'default: "DYKWDII-OUT [[DD].[MM].[YYYY]]"'
    ))
    parser.add_argument('-e', '--extension', type = str, help = (
        'the extension of the file; must be a video format supported by FFmpeg - would recommend leaving this as default\n'
        'default: ".mp4"'
    ))

    # Supply the non-NoneType arguments to the write function.
    writeMeme(**vars(parser.parse_args()))
