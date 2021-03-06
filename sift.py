#!/usr/bin/env python3

import argparse
import configparser
import config
import os

import lib

def recurse(path, conf, assemblePath):
    from lib import fileutils
    
    if os.path.isfile(path):
        fileutils.doSomethingWithFile(path, assemblePath(conf, path), conf['file_operation'])

    else:
        for root, subFolders, files in os.walk(path):

            for folder in subFolders:
                if not folder.startswith('.'):
                    recurse(os.path.join(root,folder), conf, assemblePath)

            for filename in files:
                if not filename.startswith('.'):
                    original_path = os.path.join(root, filename)
                    fileutils.doSomethingWithFile(original_path, assemblePath(conf, original_path), conf['file_operation'])

# Parse Arguments
parser = argparse.ArgumentParser(description='Move files based on perceived or existing metadata.')
parser.add_argument('paths', metavar='PATH', nargs='*', help='Sort a file/folder and let sift determine what type of file it is.')
parser.add_argument('--file', '-f', metavar='PATH', nargs=1, action='append', help='Sort a file/folder and let sift determine what type of file it is.')
parser.add_argument('--video', '-v', metavar='PATH', nargs=1, action='append', help='Sort file/folder as video')
parser.add_argument('--audio', '-a', metavar='PATH', nargs=1, help='Sort file/folder as audio')
args = parser.parse_args()

# Parse Configuration file
conf = config.config

if args.paths is not None:
    from lib import file
    for f in args.paths:
        recurse(f, conf, file.process)

if args.file is not None:
    from lib import file
    for f in args.file:
        recurse(f[0], conf, file.process)

if args.audio is not None:
    from lib import audio
    for a in args.audio:
        recurse(a, conf, lib.audio.assemblePath)

if args.video is not None:
    from lib import video
    for v in args.video:
        recurse(v[0], conf, video.process)

if args.video is None and \
   args.audio is None and \
   args.file is None and \
   args.paths is None:
    from lib import watch
    watch.start(conf) 


