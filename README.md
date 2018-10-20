# 370a3: File Versioning System
An assignment for SOFTENG370 involving editing a file system to include versioning, alongside other tools to help with versioning.

## Running and displaying the data
In Linux, you must create a directory called `mount` in the directory on which these files are located. Then run the file `versionfs.py` by navigating to the directory in which it is located via. the command line, and running the following command:
```
python ./versionfs.py mount
```
This will start producing output where it records what's going on in the filesystem. Open another terminal, navigate to the directory which `versionfs.py` is located, and start changing the files in `mount`.
For instance, try creating a file called `one.txt` in `mount`, and seeing what it produced by the other terminal displaying the output of the filesystem.

After you are done, run the following code in the second terminal:
```
fusermount -u mount
```
This will stop the file system.




## Versioning Tools
There are 5 versioning tools which you can use to aid your usage and/or testing of the file versioning system.
```
./listversions one.txt
```
Will list all the stored versions of `one.txt` (up to 6).

```
./mkcurrent one.txt 2
```
Will make the second verson of the `one.txt` the current version.

```
./catversion one.txt 3
```
Will display the contents of version three of `one.txt`.

```
./rmversions one.txt
```
Will remove all versions of `one.txt`, except the latest one (version one).

```
./shutdownversions
```
Will clear out all the directories created by the file versioning system, including the base directory `.versiondir`. It also calls `fusermount -u mount`.
