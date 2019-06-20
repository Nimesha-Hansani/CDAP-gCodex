import os


def getListOfFiles(dirName):

    listOfFile = os.listdir(dirName)
    allFiles   = list()

    #Iterate over all th entries
    for entry in listOfFile:
      # Create full path
      fullPath = os.path.join(dirName , entry)

      #If Entry is a directory then get the list of files in this directory

      if os.path.isdir(fullPath):
        allFiles = allFiles + getListOfFiles(fullPath)
      else:
        allFiles.append(fullPath) 

    return allFiles








         
    