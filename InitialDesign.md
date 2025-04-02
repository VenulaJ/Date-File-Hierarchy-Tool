''' 
use api to get current date time?

get user input for directories where the files we need to organize are stored, where we will store the new folder/file heiarchy, and the name of the Master folder we will create in the new directory

search to see both directories exist
"directory validation funtion?"
if valid, proceed past "if not, prompt..."
    elif not, prompt user to try again (error, "x (and y) directories do not exist or a grammatical error may exist)
    
check the system has enough storage on disk to complete the operation, by comparing the size of the original directory to the size of the available disk space + (estimation for amount of space taken up by the new folders) + 2%(of available disk space) ("saving room here to not overload the disk") where the new directory will be created
if there isnt enough room, prompt the user to change the target directory for the file heiarchy
move into the valid directory

create the master folder
verify the master folder was created successfully
move into the directory where the files to be organized are located

pick any item in the directory
check the current item is file
if file, continue past the "if folder, skip..."
    elif folder, skip and store keys to identify these for use in log
repeat as necessary for each item in the directory

check to see if the file is corrupt?
if not corrupt, proceed past "if corrupt, print..."
if corrupt, print message alerting the user that this file cannot be used and store a key to identify the invalid files (for printing a log with errors and description of the corrupt files)

check the size of the file
read date time of the file
create folder that corresponds to the year of the file
move into the year file
check the first file was created successfully
create another folder for the month of the file
move into the month file
check the second file was created successfully

copy the first file into the folder
verify the file copied matches the original file
if they match delete the old one
if not just delete the new corrupted file and try again, printing an error message alerting the user, store info in log
'''
