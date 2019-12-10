# Software Engineering
Software Engineering Class

Created by and maintained by Jonathan Ray

- Dataset taken from: https://www.kaggle.com/currie32/crimes-in-chicago
- Dataset has been cleaned and the date-time format has been modified to fit that of the sqlite standard

NOTE: You can find all source files for this maintained at my public github repo: 
	*** https://github.com/kingslurp/ChicagoCrime.git ***

NOTE: Executable versions, packaged with the linux / windows versions of the publicly available "PyInstaller" tool can be found at this public Google Drive link:
	*** https://drive.google.com/drive/folders/1ECXMIAvCYkp5mxFpgYpNvVbcAGer5YJ4?usp=sharing ***

Open Source Libraries and Versions Used:
1. geopy - version 1.20.0 - Used as it is a global geolocation database containing the ability to return the geolocation (lat, long) of a street adress, to return the closest known street address to a gelocation, and to compute the "Great-circle" distance between two sets of geolocation coordinates.
2. PySimpleGui - version 4.10.0 - Used to display the GUI. It is built on the standard libary in Python 3.7 called "tkinter", but tkinter was removed from our development due to known bugs with displaying some items in Mac OS X.
3. PyInstaller - version 3.5 - Used to compile the .py (Python) files in to .pyc files and to create an executable, redistributable version of the program. This was preferrable as some Python libraries such as PySimpleGui have prerequesites which prevented the creator from just copy / pasting the library folders into the same folder as the python file and running them. 



# Start Here:

1. Download the appropriate executable version from the Google Drive link above. 
	A. For Windows users, download and extract: ChicagoCrimeViewr_Windows.zip
	B. For Linux users, download and extract: ChicagoCrimeViewr_Linux.zip
2. Once you have extracted the folder, all the contents should now be in a folder of the same name, minus the ".zip" exension. Open the folder, ChicagoCrimeViewr, and run the executable.
	A. For Windows, run "ChicagoCrimeViewr.exe"
	B. For Linux, execute "ChicagoCrimeViewr". This can be done by opening a new terminal window and navigating to the directory where you extracted the contents. Then type, "./ChicagoCrimeViewr", and press Return


# General Use:
1. Starting from left-to-right, select all of the items in the list on the left-hand side by clicking each individual item that you desire to have displayed as a tooltip or popup when you click each individual plotted point in the map.
2. The remaining options are filters that can be used to filter the data you want returned from the database.
	A. The date range Start and End are already set to the minimum and maximum time frames
	B. The address field needs an address within Chicago city limits. If you do not know one, you can use the address of Chicago City Hall (121 N LaSalle St Chicago Illinois 			60602). A good default distance is 2 miles.
	C. Once you have entered all filters that you would like, press "Submit"
	D. Now navigate to the directory where you extracted the contents under the "Start Here" section, number 2.
	E. Open the newly generated report.html file in your favorite browser, and enjoy!


-- Open the /ChicagoCrimeViewr/ directory and open the "report.html" that has been generated in your favorite web browser. This should display a map with all of the plotted points returned from the generated query by the GUI backend.


+++Directory Structure of the executable/downloadable version (Taken from Windows Version)+++
->ChicagoCrimeViewr
-->(There are more files here than explained as some are required library files)
-->ChicagoCrimeViewr.exe - executable file compiled from .py (Python) files using a tool called PyInstaller
-->chicagocrime.db - SQLite Database file created from the dataset above (kaggle)
-->hacker.png - Used as the image of all returned results from the database query in the HTML report
-->house.png - Used as the image of the address that the user typed in, if the user typed an address at all

+++Directory Structure of the source code Project folder+++
-> ChicagoCrime
--> ChicagoCrimeViewr.py - This is the source code file, coded in Python3.7, used to generate the Graphical User Interface. This interface takes user input and generates a SQLite query based on the entered parameters. It then executes the query and generates a report.html in the same directory with all of the items being displayed on a map.
--> db_format.txt - Contains TODO items and known bugs
--> hacker.png - same as description above in executable directory structure
--> house.png - same as description above in executable directory structure
-- README.md - THIS FILE

