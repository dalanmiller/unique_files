### unique_files

I wrote this script for a company in order to go through a directory recursively and find all the unique file names which could be repeated throughout the different folders. There are some exceptions as the system used used some file names which should also be kept rather than overwriting newer versions of the file. I am proud of this work for the most part because I didn't know about os.path.walk at the time and I believe (to an extent) wrote my own version of it for our purposes. 

In essence, the script consists of two parts, the first which scans through the origin folder for all the files and puts their names as the keys and paths as the values into a dictionary.

This dictionary is then passed to the second part of the script which takes the dictionary and the destionation path and moves all the files one at a time to the destination. After all the files have been moved it ensures that the original files and the files at the destination directory are the same before ending. 

To ensure that there will be no overlap a new folder is created within the given destination directory with a name based on the current time the script is run. The idea being that the script could be automated and have a degree of assurance that it wouldn't step on its own toes. 

## The script makes use of the following modules:

* time - for naming files and folders as well as making sure that the copied files will always be in a uniquely named folder (with the exception that the script is run within the same second which in our environment would be near-enough-unlikely to happen) 
* sys - Solely for argv and being able to call the script from the command line and pass it paths to run rather than hard coding then running. It was my own attempt to enabling the functionality of other modules that offer much more robust command line argument functionality.
* os - Needed the os module to navigate through directories ensure that certain paths were files or folders
* re - This was the first script that I created using regular expressions and was quite happy with the results. Although I think my patterns could be optimized, it quickly accomplished what I needed to do.
* pprint - for printing prettily to my custom log files. 
* shutils - for using python's builtin libraries for copying files rather than using a system command through os.system or os.popopen. More portable this way. 
* filecmp - for comparing the original files and destination directory, proved useful in showing errors that didn't appear elsewhere when doing the file compare process. 


