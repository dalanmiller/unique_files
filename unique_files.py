
from time import strftime, localtime
from sys import argv
import os
import re
from pprint import pprint
from shutil import copyfile
from filecmp import cmp

#SPECIALS contains a list of files that are very common and need to be uniquely saved
SPECIALS = ['build.xml'] 


def folder_scan(path):
	"""
	Initializes a dictionary which keys are added based on the file names in that directory and values are the full path to that file

	If the for loop comes across a folder, folder_scan is called recursively on the contents of that folder and henceforth.
	"""

	file_dict = {}
	
	dir_list = os.listdir(path)
	
	#Pre-compile for speed!
	r = re.compile(r"[-,_].+") 
	b = re.compile(r"build.xml")
		
	dir_list.sort() #Sorts the contents of this directory in order to ensure that newer folders come later and override earlier-scanned files
	
	for x in dir_list: 
		
		#If target is both a directory and hypen or underscore is in the folder name
		if os.path.isdir(os.path.join(path,x)) and re.search(r, x): 
			
			a = folder_scan(os.path.join(path,x))
			

			#For files within a folder that is -hot, -tnt etc will append that suffix to the end of the key in the dict UNLESS it is a build.xml file.
			for z in [x for x in a.keys() if not re.search(b, x)]:
				
				#Takes the file key and appends the -hot8pm suffix to it and gives it the value of the original key
				a["%s_%s" % (z, path.rsplit('/')[-1])] = a[z]
				
				#Removes original key (and thus value)
				a.__delitem__(z)
			
			#Updates parent dictionary
			file_dict.update(a)

		#If target is directory but doesn't contain a build suffix (-hot, -8pm, etc)
		elif os.path.isdir(os.path.join(path,x)):
		
			#Updates the local dictionary with the returned dictionary of the folder_scan
			file_dict.update(folder_scan(os.path.join(path,x))) 
		
		elif os.path.isfile(os.path.join(path,x)) and x in SPECIALS:
		#If the file name is a special file such as build.xml, it finds the date folder via regex and appends it to the end of the file

			if x == "build.xml":
				#Appends the previous two directory names to the end of the build.xml key which will change the file name later on
				file_dict["%s_%s_%s" % (x.lower(),path.rsplit("/")[-1].lower(), path.rsplit("/")[-2].lower())] = os.path.join(path,x)
		
		#exception for files within cattext
		#elif re.search("CatText",os.path.join(path,x):
			
			

		#Target is a file
		elif os.path.isfile(os.path.join(path,x)):
			
			#Normal file = adds it into the dictionary
			file_dict[x.lower()] = os.path.join(path,x)

	#Return completed dictionary
	return file_dict
	
def copy_files(webster, dest):
	""" 
	Takes a dictionary of keys of file names and values of full paths and a final destination path 
	then copies all the files to final destination path as the string stored as the key. 
	"""
	assert isinstance(webster,dict) #Checks if path given is a directory and if webster is a dictionary

	assert os.path.exists(dest)
		
	#Creates dated folder within folder specified to put files.
	date = strftime("%a %b %d", localtime())
	date_dest = os.path.join(dest,strftime("%a_%b_%d_%H%M%S", localtime())+"_archive")

	#Creating directory
	print "Creating directory: "+date_dest 
	os.mkdir(date_dest)
	
	#Worried that log won't be available outside the following if statement
	log = '' 
	
	#Creating __backup.log 
	backup_path = os.path.join(date_dest,"__backup.log")

	log = open(backup_path,'w')
	log.write("PROPOSED ARCHIVE OF "+date+"\n")
	for key,value in webster.iteritems():
		log.write("%s - %s\n" % (key,value))

	print "Copying..."
	log.write("BEGIN FILE COPY\n")

	for key, value in webster.iteritems():
		try:
			#File copy command
			copyfile(value,os.path.join(date_dest,key)) 
				
			#Writing to log success
			log.write("Success: "+value+"\n") 

		except:
			log.write("Error: "+value+"\n")
			#fail.update({x:webster[x]})
			print("Copy Error: "+value+"\n")
			
	
	print "Comparing..."
	#log = open(os.path.join(dest,strftime("%a_%b_%y_%H%M%S", localtime())+"_archive/__backup.log"), 'w'
	log.write("BEGIN FILE COMPARISON CHECK\n")

	for key,value in webster.iteritems():
				
		if cmp(value,os.path.join(date_dest,key)):
			
			log.write("poscmp:")

		else:
			
			log.write("negcmp:")
			print("Neg Compare: "+value+" => "+os.path.join(date_dest,key))

		log.write(" %s => %s \n" % (value, os.path.join(date_dest,key)))

	log.close()

if __name__ == "__main__":
	assert(os.path.isdir(argv[1]))
	assert(os.path.isdir(argv[2]))
	
	try:
		q = folder_scan(str(argv[1]))
		copy_files(q, str(argv[2]))
		compare_files(q,str(argv[2]))
		print "Complete"	

	except:
		print "Something went wrong, please check your provided directories"
