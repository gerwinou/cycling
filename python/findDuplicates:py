# Import the os module, for the os.walk function
import os
import hashlib
import time

start = time.time()
# Set the directory you want to start from
rootDir = 'c:\\test\\'


Dict1 = {}
Dict2 = {}

outResult = open("e:\\log.txt","w")

for dirName, subdirList, fileList in os.walk(rootDir):
 #   print('Found directory: %s' % dirName)
    for fname in fileList:
		#print('\t%s' % fname)
		tbd = os.path.join(dirName, fname)
		#print tbd
		file_to_check = open(tbd)
		#print file_to_check
		dat = file_to_check.read()
		#print dat
		sha1sum = hashlib.md5(open(tbd, 'rb').read()).hexdigest()
		#sha1sum = hashlib.sha1(dat).hexdigest()
		#file_to_check.close()
		#print sha1sum

		if (sha1sum in Dict1.values()):
			#print("Already present " + tbd)
			outResult.write("duplicate of:" + Dict2[sha1sum] + "\n")
			outResult.write("duplicate:" + tbd + "\n")
		else:
			Dict1[tbd] = sha1sum
			Dict2[sha1sum] = tbd

#print Dict1
outResult.close()
end = time.time()
totaltime = end - start
print(totaltime)
