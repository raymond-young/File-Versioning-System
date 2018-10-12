#!/usr/bin/env python
from __future__ import with_statement

import logging

import os
import sys
import errno

# Added
import shutil
import filecmp

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn


class VersionFS(LoggingMixIn, Operations):
    def __init__(self):
        # get current working directory as place for versions tree
        self.root = os.path.join(os.getcwd(), '.versiondir')
        # check to see if the versions directory already exists
        if os.path.exists(self.root):
            print 'Version directory already exists.'
        else:
            print 'Creating version directory.'
            os.mkdir(self.root)

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        #print "access:", path, mode
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        #print "chmod:", path, mode
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        #print "chown:", path, uid, gid
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        #print "getattr:", path
        full_path = self._full_path(path)

        st = os.lstat(full_path)
        # print st
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    # returns all the files in the specified directory (current, if unspecified)
    def readdir(self, path, fh):
        #print "readdir:", path
        full_path = self._full_path(path)
        # print full_path

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            # print r
            if r.endswith('.txt'):
                yield r

    def readlink(self, path):
        #print "readlink:", path
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        #print "mknod:", path, mode, dev
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        #print "rmdir:", path
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        #print "mkdir:", path, mode
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        #print "statfs:", path
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        #print "unlink:", path
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        #print "symlink:", name, target
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        #print "rename:", old, new
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        #print "link:", target, name
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        #print "utimens:", path, times
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        print '** open:', path, '**'
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print '** create:', path, '**'
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print '** read:', path, '**'
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print '** write:', path, '**'
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print '** truncate:', path, '**'
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print '** flush', path, '**'
        return os.fsync(fh)

    # TODO
    def release(self, path, fh):
        print '** release', path, '**'

        # Check if a 'version' exists. If not, then make one
        r = []
        if os.path.isdir(self.root):
            r.extend(os.listdir(self.root))

        # Ignore .swp files
        for i in r:
            if i.endswith('.swp') or i.startswith('.'):
                r.remove(i)

        #r = self.readdir("",fh)
        print r
        # print "Here1"

        # The name of 'version 1' of the file
        _version1 = path + '.1'
        print 'Version: ' + _version1
        print 'Original: ' + path

        exists = False
        file_versions = [] # All the versions of the path file.
        for i in r:
            print 'i =' + i
            if (_version1 == '/' + i):
                exists = True
                #print 'This is the first version: ' + '/' + i
            # If they're a version, then add them to the array
            if ('/' + i).startswith(path) and (i.endswith('.1') or i.endswith('.2') or i.endswith('.3') or i.endswith('.4') or i.endswith('.5') or i.endswith('.6')):
                file_versions.append(i)
                #print 'This one is a version: ' + i


        # Copy the file into a new 'versioned' file.
        if (exists == False) and not(path.endswith('.swp')) and not (path.startswith('.')):
            shutil.copyfile(self._full_path(path), self._full_path(_version1))
            file_versions.append(i)
            print 'Created new version thing'

        print 'Version FULL: ' + self._full_path(_version1)
        print 'Original FULL: ' + self._full_path(path)
        #print 'Versions: ' + file_versions

        print 'Are they the same?'
        # Check if there were any changes made.
        if (filecmp.cmp(self._full_path(_version1), self._full_path(path)) == False):
            print 'Theyre different!'
            # If a change was made, then shift all the version numbers by one,
            # and make the changed one the latest version.
            for ver in file_versions:
                # Copy the contents into some temporary files, then rename.
                shutil.copyfile(self._full_path(ver), self._full_path(ver) + 'temp')

            for ver in file_versions:
                if (ver.endswith('.1')):
                    shutil.copyfile(self._full_path(ver) + 'temp', self._full_path(path + '.2'))
                    os.remove(self._full_path(ver) + 'temp')
                    print 'Moved 1 over.'
                if (ver.endswith('.2')):
                    shutil.copyfile(self._full_path(ver) + 'temp', self._full_path(path + '.3'))
                    os.remove(self._full_path(ver) + 'temp')
                    print 'Moved 2 over.'
                if (ver.endswith('.3')):
                    shutil.copyfile(self._full_path(ver) + 'temp', self._full_path(path + '.4'))
                    os.remove(self._full_path(ver) + 'temp')
                    print 'Moved 3 over.'
                if (ver.endswith('.4')):
                    shutil.copyfile(self._full_path(ver) + 'temp', self._full_path(path + '.5'))
                    os.remove(self._full_path(ver) + 'temp')
                    print 'Moved 4 over.'
                if (ver.endswith('.5')):
                    shutil.copyfile(self._full_path(ver) + 'temp', self._full_path(path + '.6'))
                    os.remove(self._full_path(ver) + 'temp')
                    print 'Moved 5 over.'
                if (ver.endswith('.6')):
                    #os.remove(self._full_path(ver)) # Don't actuallly need to delete, since it's overwritten.
                    os.remove(self._full_path(ver) + 'temp')
                    print 'Deleted 6.'

            shutil.copyfile(self._full_path(path), self._full_path(path + '.1'))
            print 'Moved new file over. Sweet'

        # (Try) hide the versioning files from being seen
        #for ver in file_versions:
           #self.chmod(self._full_path(ver), 000)
            #os.remove(self._full_path(ver) + '../mount/' + path)
            #print 'Hopefully that changed the file permissions.'

        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print '** fsync:', path, '**'
        return self.flush(path, fh)


def main(mountpoint):
    FUSE(VersionFS(), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1])
