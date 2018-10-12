#!/usr/bin/env python
from __future__ import with_statement

import logging

import os
import sys
import errno

import shutil
import filecmp

from subprocess import call

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn


class ShutDownVersions():
    def __init__(self):
        # get current working directory as place for versions tree
        self.root = os.path.join(os.getcwd(), '.versiondir')
        self.mountdir = os.path.join(os.getcwd(), 'mount')

        shutil.rmtree(self.root)
        call(['fusermount', '-u' ,'mount'])


    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path




def main():
    ShutDownVersions()

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main()
