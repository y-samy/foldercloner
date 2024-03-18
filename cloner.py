import os
from glob import glob


def obtainDirectories(TYPE, DirToMatch):
    prompts = ["Please enter the path of the original folder:\n> ", "Please enter the path of the EMPTY clone folder:\n> "]
    dirValid = False
    prompt = prompts[TYPE]
    
    directory = str(input(prompt)).strip("\\").strip("/")
    while dirValid == False:
        if os.path.exists(directory) and TYPE == 0:
            dirValid = True   
        elif TYPE == 1:
            if not os.path.exists(directory):
                print("This folder was not found. Press ENTER to create it or type another folder location:")
                choice = input("> ")
                if choice == "":
                    os.mkdir(directory)
                    dirValid = True
                else:
                    directory = choice
            elif os.path.samefile(directory, DirToMatch):
                print("The clone folder can't be the same as the original folder. Please try again...")
                directory = str(input(prompt)).strip("\\")
            else:
                dirValid = True

        else:
            print("Directory doesn't exist or insufficient permissions. Please try again...")
            directory = str(input(prompt)).strip("\\")
            
    return directory


def discoverFolders(DIR):
    print("Discovering folders in the source directory...")
    listOfFolders = []
    pathsOfFolders = glob(str(DIR + "/**/"), recursive=True, include_hidden=True)
    for folder in pathsOfFolders[1:]:
        folder = folder[len(DIR):]
        print("Found folder '" + folder + "'")
        listOfFolders.append(folder)
    return (listOfFolders, pathsOfFolders)
    
def createFolders(SDIR, TDIR):
    print("Creating empty folders...")
    listOfFolders, pathsOfFolders = discoverFolders(SDIR)
    for folder in listOfFolders:
        print("Making folder " + str(TDIR + folder))
        os.mkdir(str(TDIR + folder))
    return (pathsOfFolders, SDIR, TDIR)

def discoverFiles(DIR, pathsOfFolders):
    print("Discovering files in the source directory...")
    pathsOfFiles = glob(str(DIR + "/**/*"), recursive=True, include_hidden=True)
    for folder in pathsOfFolders:
        if folder.strip("\\") in pathsOfFiles:
            pathsOfFiles.remove(folder.strip("\\"))
    listOfFiles = []
    for file in pathsOfFiles:
        file = file[len(DIR):]
        listOfFiles.append(file)
    return (pathsOfFiles, listOfFiles)

def populate(pathsOfFolders, SDIR, TDIR):
    pathsOfFiles, listOfFiles = discoverFiles(SDIR, pathsOfFolders)
    for index, file in enumerate(listOfFiles):
        file = str(TDIR + file)
        print(pathsOfFiles[index])
        command = str("cmd /c \" mklink /H " + "\"" + file + "\" \"" + pathsOfFiles[index] + "\" \"")
        os.system(command)


def main():
    sourceDir = obtainDirectories(int(0), "")
    targetDir = obtainDirectories(int(1), sourceDir)
    populate(*createFolders(sourceDir, targetDir))
    
    
main()
