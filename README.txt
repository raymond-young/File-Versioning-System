Heres what to do if you forget

This command compiles your file to an executable (with no file extension).
You'll have to look up the absolute path for it to work though.
Go 
sudo find / -name pyinstaller

Then paste that address in this line:
/my/path/to/pyinstaller --onefile <yourscriptname>.py

This will give you the executable in the dist folder, which you should move to the main folder. You can run it like this:

./<scriptname> [arg1] [arg2]




OTHER STUFF
This starts the file system:
python versionfs.py mount

This stops it:
fusermount -u mount

Read the .pdf if you forget what any of the executables does. Cool.

