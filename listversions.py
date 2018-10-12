#!/usr/bin/env python
from __future__ import with_statement

import logging

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn


class ListVersions():
    def __init__(self):
        # get current working directory as place for versions tree
        self.rootdir = os.path.join(os.getcwd(), '.versiondir')
        self.mountdir = os.path.join(os.getcwd(), 'mount')
        # check to see if the versions directory already exists
        #if os.path.exists(self.rootdir):
        #    print 'Version directory already exists.'
        #else:
        #    os.mkdir(self.rootdir)
        #    print 'Creating version directory.'

        r = []
        # Get the files in .versiondir that are the versions of fileName.
        if os.path.isdir(self.rootdir):
            r.extend(os.listdir(self.rootdir))

        # Ignore .swp files
        for i in r:
            if i.endswith('.swp') or i.startswith('.'):
                r.remove(i)

        #print r
        path = sys.argv[1]
        #print 'Original: ' + path

        file_versions = [] # All the versions of the path file.
        for i in r:
            # print 'i =' + i
            # If they're a version, then add them to the array
            if (i).startswith(path) and (i.endswith('.1') or i.endswith('.2') or i.endswith('.3') or i.endswith('.4') or i.endswith('.5') or i.endswith('.6')):
                #file_versions.append(i)
                print i


    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path




def main(fileName):
    ListVersions()

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1])
