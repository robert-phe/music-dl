#!/usr/bin/env python
# coding: utf-8

import argparse
import os

import clipboard

from music_dl.MusicDL import MusicDL


def version():
    curdir = os.path.abspath(os.path.dirname(__file__))
    pardir = os.path.abspath(os.path.join(curdir, os.pardir))
    version_file = os.path.join(pardir, 'VERSION')
    with open(version_file, encoding='utf-8') as f:
        return f.read()


__copyright__ = 'Copyright (C) 2018 Gumob'
__version__ = version()
__license__ = 'MIT'
__author__ = 'Gumob'
__author_email__ = 'hello@gumob.com'
__url__ = 'http://github.com/gumob/music-dl'


def main():
    # Version
    version_file = os.path.abspath(os.path.basename(__file__) + '/../VERSION')
    with open(version_file) as f:
        progver = f.read().strip()
    progver = 'music-dl {}'.format(progver)

    # Default working directory
    default_dir = os.path.expanduser('~/Music/Downloads')

    # Parse arguments
    parser = argparse.ArgumentParser(
        prog='music-dl',
        description='Music Downloader - Command line tool to download music from YouTube and SoundCloud',
        add_help=False,
        epilog=progver
    )
    parser.add_argument('-u', '--url', help='URL to download. Without this argument, URL is read from clipboard.', type=str)
    parser.add_argument('-d', '--dir', help='Full path to download directory. Default value is {}.'.format(default_dir), type=str)
    parser.add_argument('-ac', '--codec', help='Preferred audio codec. [available=m4a,mp3,flac default=m4a]', type=str, default='m4a')
    parser.add_argument('-ab', '--bitrate', help='Preferred audio bitrate. [default=198]', type=int, default=198)
    parser.add_argument('-ps', '--playlist-start', help='Index specifying playlist item to start at. [default=1 (index of first song on playlist)]', type=int, default=1)
    parser.add_argument('-pe', '--playlist-end', help='Index specifying playlist item to end at. [default=0 (index of last song on playlist)]', type=int, default=0)
    parser.add_argument('--no-artwork', help='Forbid adding artwork to audio metadata.', action='store_true')
    parser.add_argument('--no-track-number', help='Forbid adding track number to audio metadata.', action='store_true')
    parser.add_argument('--no-album-title', help='Forbid adding album title to audio metadata.', action='store_true')
    parser.add_argument('--no-album-artist', help='Forbid adding album artist to audio metadata.', action='store_true')
    parser.add_argument('--no-composer', help='Forbid adding composer to audio metadata.', action='store_true')
    parser.add_argument('--no-compilation', help='Forbid adding part of compilation flag to audio metadata.', action='store_true')
    parser.add_argument('--open-dir', help='Open download directory after all songs are downloaded.', action='store_false')
    # parser.add_argument('--clear-cache', help='Clear cache directory.', action='store_true')
    parser.add_argument('--verbose', help='Print verbose message.', action='store_true')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    args = parser.parse_args()
    args.url = args.url if args.url is not None else clipboard.paste()
    args.dir = args.dir if args.dir is not None else default_dir

    # Execute download
    with MusicDL(
            download_url=args.url,
            working_dir=args.dir,
            audio_codec=args.codec,
            audio_bitrate=args.bitrate,
            playlist_start=int(args.playlist_start),
            playlist_end=int(args.playlist_end),
            no_artwork=args.no_artwork,
            no_album_title=args.no_album_title,
            no_album_artist=args.no_album_artist,
            no_track_number=args.no_track_number,
            no_composer=args.no_composer,
            no_compilation=args.no_compilation,
            open_dir=args.open_dir,
            # clear_cache=args.clear_cache,
            verbose=args.verbose,
    ) as mdl:
        mdl.download()
