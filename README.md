Software Dependancies:
----------------------

Python 2.7.10



Modules Dependancies:
---------------------
Standard Python packages 
	- sys
	- os
	- re

*No other python modules used inside the code.  



Instructions to run the code:
-----------------------------
- Code assumes it will be run from folder where it can see input, output and src
- It will create output folder if it doesn;t exists
- It will overwrite any output files that are pre existing 


Sample run command:
-------------------
Path: $CWD

python ./src/find_political_donors.py input/itcont.txt  output/medianvals_by_zip.txt ./output/medianvals_by_date.txt



Implementation:
---------------
- The code reads the input file line by line 
- It creates a dictionary dataByZipCode, where it stores Total dollars for given name and zip code in dataByZipCode[name, zip_code, dollars] and count in dataByZipCode[name, zip_code, count]
- When processing each line it parallely prints total dollar amount for given name and running median
- It also creates another dictionary dataByDate, where it stores data by name and date
- After processing all the data it sorts the dictionary and prints it to medianvals_by_date.txt file
- Tested the code with huge Dataset having 4.5M lines, and it could complete in a minute in my laptop 

