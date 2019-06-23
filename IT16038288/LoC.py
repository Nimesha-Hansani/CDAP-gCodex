commentSymbol = '#' or '//' 

import sys
import os, os.path



currentDir = "F:/4th year Research/1-The Project/50%/CDAP-gCodex/Repo_Clonning/WriteFiles.py"
#currentDir = os.getcwd()
 
filesToCheck = ['WriteFiles.py']
#for root, _, files in os.walk(currentDir):
    #for f in files:
        #fullpath = os.path.join(root,f)
        

#if not filesToCheck:
 #   print ("No files found.")
  #  quit()

lineCount = 0
totalBlankLineCount = 0
totalCommentLineCount = 0

print("")
print ("Filename\tlines\tblank lines\tcomment lines\tcode lines")

for fileToCheck in filesToCheck:
    with open(currentDir) as f:

        fileLineCount = 0
        fileBlankLineCount = 0
        fileCommentLineCount = 0

        for line in f:
            lineCount += 1
            fileLineCount += 1

            lineWithoutWhitespace = line.strip()
            if not lineWithoutWhitespace:
                totalBlankLineCount += 1
                fileBlankLineCount += 1
            elif lineWithoutWhitespace.startswith(commentSymbol):
                totalCommentLineCount += 1
                fileCommentLineCount += 1

        print (os.path.basename(fileToCheck) + \
              "\t" + str(fileLineCount) + \
              "\t" + str(fileBlankLineCount) + \
              "\t" + str(fileCommentLineCount) + \
              "\t" + str(fileLineCount - fileBlankLineCount - fileCommentLineCount))

#print("")
#print ("Filename\tlines\tblank lines\tcomment lines\tcode lines")
print ("")
print ("Totals")
print ("--------------------")
print ("Lines:         " + str(lineCount))
print ("Blank lines:   " + str(totalBlankLineCount))
print ("Comment lines: " + str(totalCommentLineCount))
print ("Code lines:    " + str(lineCount - totalBlankLineCount - totalCommentLineCount))