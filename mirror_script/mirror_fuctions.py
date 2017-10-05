import os
from multiprocessing import Pool
import csv
import subprocess
import time


listy = []
subDirectoryList = []


def get_immediate_subdirectories(a_dir):
    #return [x for x in os.listdir(a_dir)]         gives authentication error
    #listy = [os.path.abspath(name) for name in os.listdir(a_dir) if os.path.isdir(name)] gives socket is not connected error
    #listy = [x[0] for x in os.walk(a_dir)]         gives no error but says there is nothing there
    #listy = [x for x in filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))]    no such file/directory error
    #listy = [x.path for x in os.scandir(a_dir) if x.is_dir()]  no

    return listy


def parallelProcess(mirror_directory):
    walk = os.walk(mirror_directory)
    if os.listdir(mirror_directory) == []:  # if there is nothing in the directory given by dirname
        listy.append((mirror_directory, ""))
    for roots, dirs, files in walk:
        for file in files:
            path = os.path.join(roots, file)
            listy.append((path, file))
    return listy



def mirror_files_recursive(lst):
    output_dir = '/Users/Selen/Subject_Files_Test'
    #for subList in lst:
    for tup in lst:
        #print(tup)
        filepath = tup[0]
        #print("tup[0] is " + tup[0])
        base_name = os.path.basename(filepath)
        drive, localdir = os.path.splitdrive(filepath)
        savepath = os.path.join(output_dir, os.path.normpath(os.path.dirname(localdir)).lstrip(r"\\").lstrip("/"))
        try:
            with open(savepath):
                pass
        except IOError:
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            pathBefore = os.getcwd()
            os.chdir(savepath)
            try:
                subprocess.call(['touch', base_name])
            except WindowsError:
                open(base_name, 'a').close()
            os.chdir(pathBefore)
    print("Successfully mirrored!")


if __name__=="__main__":
    start_time = time.time()
    subList = []
    with open('subdirectories.txt', 'rt') as csvfileR:

        pReader = csv.reader(csvfileR, delimiter='\t', quotechar='|')
        for row in pReader:
            subList.append(row)
        subList = [x[0] for x in subList]


    for y in subList:
        subDirectoryList.append('/Volumes/psych/BergelsonLab/Scripts_and_Apps/Subject_Files/' + y)

    pool = Pool(processes=51)
    listthing = pool.map(parallelProcess, subDirectoryList)

    #newListThing = [(x, '/Users/Selen/Subject_Files_Test') for x in listthing]
    pool.map(mirror_files_recursive, listthing)

    #mirror_files_recursive(listthing, '/Users/Selen/Subject_Files_Test')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Total time: " + str(elapsed_time))



