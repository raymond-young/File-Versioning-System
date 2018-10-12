#!/usr/bin/env python
from __future__ import with_statement

import logging

import os
import sys
import errno

import shutil
import filecmp

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn


class CatVersion():
    def __init__(self):
        # get current working directory as place for versions tree
        self.root = os.path.join(os.getcwd(), '.versiondir')
        self.mountdir = os.path.join(os.getcwd(), 'mount')
        # check to see if the versions directory already exists
        #if os.path.exists(self.root):
        #    print 'Version directory already exists.'
        #else:
        #    os.mkdir(self.root)
        #    print 'Creating version directory.'

        r = []
        # Get the files in .versiondir that are the versions of fileName.
        if os.path.isdir(self.root):
            r.extend(os.listdir(self.root))

        # Ignore .swp files
        for i in r:
            if i.endswith('.swp') or i.startswith('.'):
                r.remove(i)

        #print r
        path = sys.argv[1]
        #print 'Original: ' + path

        versionExists = False
        file_versions = [] # All the versions of the path file.
        for i in r:
            # print 'i =' + i
            # If they're a version, then add them to the array
            if (i).startswith(path) and (i.endswith('.1') or i.endswith('.2') or i.endswith('.3') or i.endswith('.4') or i.endswith('.5') or i.endswith('.6')):
                file_versions.append(i)
                if i.endswith('.' + sys.argv[2]):
                    versionExists = True
                #print i



        #print 'Heres a thing'
        if (int(sys.argv[2]) > 0 and int(sys.argv[2])<7 and versionExists):
            f = open(self._full_path(path + '.' + sys.argv[2]) ,'r')
            file_contents = f.read()
            print file_contents
            f.close()
        else:
            print 'File doesnt exist, or version index out of bounds'
    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path




def main():
    CatVersion()

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main()
