import glob
import os
import zipfile

# usage:  "python3 filework.py" in the director where all your files are.

# This tool grabs all .txt files with "z" in the filename.
# It saves those filenames into a list without ".txt" extension.
# Then it runs the echo command just as a demo command.
# This it create creates a zip archive of the new files.

# find all files withe name containing z
# remove the txt
newlist=[]
for name in glob.glob('*z*.txt'):
     newlist.append(name.rstrip(".txt"))

# execute a command with those names
for name in newlist:
    os.system("echo zzz >> " + name)

# zip the new output
with zipfile.ZipFile('new.zip', 'w') as new_zip:
    for name in newlist:
        new_zip.write(name)
 
