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


## File Versioning
All files stored in the `mount` directory will be versioned. The latest 6 versions of the file will be stored in the hidden directory `.versiondir`, named according to the version number (e.g. `yourfile.txt.1` is the latest version of `yourfile.txt`). Upon creating a seventh version of the file, the oldest version will be deleted.

Try creating a file in the `mount` directory, then making some edits to it. Watch what happens in the first terminal (the one running `python .versionfs.py mount`).
```
one > mount/one.txt
nano mount/one.txt
```
Make some edits, then close nano (the text editor).
If the file in `mount` is deleted, the versioned files will still remain. This way, you can recover files if they are accidentally deleted.



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
