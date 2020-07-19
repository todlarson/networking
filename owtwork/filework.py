import glob
import os
import zipfile

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
 
