#!/usr/bin/python
import sys
import os
import re

def main ():
	#Record start time
	start = os.popen("date +%s").read()
	
	## Parse Input options 
	ifile, byZip, byDate = parse_options()
	
	## Process Data 
	process_data(ifile, byZip, byDate)
	
	end  = os.popen("date +%s").read()
	#print "\nCompleted Successfully, Time elapsed : " , (float(end)-float(start)) , "secs"


def custom_round (amount, count):
	div = round(float(amount)/float(count))	
	return long(div)


def process_data(ifile, byZip, byDate):
	dataByZipCode = {}
	dataByDate    = {}
	name          = ()
	isValid       = 0
	
	try:
		if(not os.path.exists("./output")):
			os.makedirs("./output")
	except:
		print "ERROR: ./output dir doesn't exists and could not create a new one"
		sys.exit(-1)
	
	try:
		o = open(byZip, "w")
	except:
		print "ERROR: Couldn't open \"", byZip, "\" file for writing "
		sys.exit(-1)
	
	# Read file
	with open(ifile) as f:
		for line in f:
			array = line.split("|")
			
			if(re.search('\w+', array[15]) or not re.search('^\w+$', array[0]) 
			or not re.search('\d+', array[14]) or not re.search('\d\d\d\d\d', array[10]) 
			or not re.search('\d\d\d\d\d\d\d\d', array[13])):
				continue
				
			zip_code = array[10][0] + array[10][1] + array[10][2] + array[10][3] + array[10][4]
			date     = array[13]
			
			
			## Check if Data exists in dataByZipCode
			if( (array[0], zip_code , 'dollars') in dataByZipCode ):
				count  = long(dataByZipCode[array[0], zip_code , 'count']) + 1
				amount = long(dataByZipCode[array[0], zip_code , 'dollars']) + long(array[14])
				avg    = custom_round(amount, count)

				o.write(str(array[0]) + "|" + zip_code + "|"+ str(avg) + "|" + str(count) + "|" + str(amount) + "\n")																	       

				dataByZipCode[array[0] , zip_code , 'dollars']  = amount
				dataByZipCode[array[0] , zip_code , 'count']    = count
			
			else:
				o.write(array[0] + "|" + zip_code + "|"+ str(array[14]) + "|" + str(1) + "|" + str(array[14])+ "\n")																	       
				dataByZipCode[array[0] , zip_code , 'dollars'] = long(array[14])
				dataByZipCode[array[0] , zip_code , 'count']   = 1
			
			
			
			# Check if Data exists in dataByDate
			if( (array[0], date , 'dollars') in dataByDate ):
				amount = long(dataByDate[array[0], date , 'dollars']) + long(array[14])

				dataByDate[array[0] , date , 'dollars']  = amount
				dataByDate[array[0] , date , 'count']   += 1
			
			else:
				dataByDate[array[0] , date , 'dollars'] = long(array[14])
				dataByDate[array[0] , date , 'count']   = 1
			
						

	o.close()
	dataByZipCode = {}
	
	# Build sort by date file	
	try:
		o = open(byDate, "w")
	except:
		print "ERROR: Couldn't open \"", byDate, "\" file for writing "
		sys.exit(-1)
	

	sorted_list = dataByDate.keys()
	sorted_list.sort(key=lambda x: (x[0], -1*int(x[1])))
	
	for key in sorted_list:
		if(re.search('count' , str(key))):
			continue
		
		total = dataByDate[key[0] , key[1], key[2]]
		count = dataByDate[key[0] , key[1], 'count']
		avg   = custom_round(total, count)

		o.write(key[0] + "|" + key[1] + "|" + str(avg) + "|" + str(count) + "|" + str(total)  + "\n")
	
	o.close()

# Parse input options 
def parse_options():   
	ifile = None
	byDate = None
	byZip  = None
	

	ifile = sys.argv[1]
	byZip = sys.argv[2]
	byDate  = sys.argv[3]
	
	if(not os.path.isfile(ifile)):
		print "ERROR: Couldn't read CSV file \"", ifile , "\"(Please check if the file exists) \n" 
		sys.exit(-1)	
	
	
	if(ifile == None):
		print ""
		print "ERROR: <CSV Data file> Not provided !!"
		sys.exit(-1) 
	
	if(byZip == None):
		print ""
		print "ERROR: <Output file medianvals_by_zip.txt> Not provided !!"
		sys.exit(-1) 
	
	if(byDate == None):
		print ""
		print "ERROR: <Output file medianvals_by_date.txt> Not provided !!"
		sys.exit(-1) 
	
	
	#print "INFO: Input sanity check passed proceeding with Data Analysis"
	return (ifile, byZip, byDate)


## Print Usage information to user and exit 
def usage(): 
	print "\nUsage: " , sys.argv[0] , " <CSV Data file> <medianvals_by_zip.txt> <medianvals_by_date.txt> "
	print "--------------------------------------------------------------"
	print ""
	print ""
	sys.exit(2)


if __name__ == "__main__":
	main()  
