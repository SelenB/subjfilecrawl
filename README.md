## Table of Contents
* [Subject File Crawler](#sfc)
  * [Mirroring Directories](#mirror)
  * [Crawling a Directory vs. Scanning a CSV](#crawlorscan)
  * [File Types](#filetypes)
  * [Filtering by Date](#date)
  * [Choosing Subjects](#subjects)
  * [Running the Subject File Crawler](#run)


# <a name="sfc"></a>Subject File Crawler

The subject file crawler application helps to access specified types of files contained within the Seedlings/Subject_Files directory.  The applications returns either a CSV file of all filepaths or copies the actual files to a specified directory (either keeping the tree structure or simply dumping the files).

## <a name="mirror"></a>Mirroring Directories 

In order to speed up the process of iterating through all of the files, we have provided an option to mirror a directory.  The options for this widget include:
* directory to mirror
* output directory
* choose between copying all files to the output directory or saving a csv containing all the file paths.

Outputting to CSV is preferred, as iterating over the CSV file is much faster than iterating through a directory.  If you choose to copy the files, the directory structure will be created, but the files will contain no content.

A success popup will appear when the mirroring process is completed.

## <a name="crawlorscan"></a>Crawling a Directory vs. Scanning a CSV

As stated previously, scanning a CSV file is much faster than recursing through a directory.  Please specify which option you are choosing by using the checkbox located at the top left of the GUI.

If you choose to pass in a CSV file, please make sure the crawl directory is pointing to a CSV file.  Similarly, if you choose to crawl a directory, make sure the crawl directory is pointing to a folder.

You once again have the choice to output to a CSV or copy the files.  Either option will create a new file/folder in your specified output directory.  If you would prefer dumping all files into your output folder instead of keeping the directory structure, please specify that by using the provided checkbox.

## <a name="filetypes"></a>File Types

You can choose as many file types as you want.  The file types (and their specific options) are shown below:

* Audio Clan Files:
    * newclan_merged_final
    * final
    * newclan_merged
    * silences
* Basic Audio Files:
    * check.csv 
* Video Datavyu Files:
    * final
    * consensus
* Basic Video Files:
    * check.csv
* Silence Files:
    * silences.txt
* Lena5min Files:
    * lena5min.csv
* Video mp4 Files:
    * *.mp4
* Audio wav Files:
    * scrubbed
    * unscrubbed
* Write your own regex:
    * please use the format r'your_regex'

## <a name="date"></a>Filtering By Date

The subject files contain data from 6 months through 18 months, which are set as the default.  If you only want a certain range of months, please specify that in the Start Month/End Month scrollbars.

## <a name="subjects"></a>Choosing Subjects

There are currently 46 subjects.  Data from all of them is selected as the default.  If you want only specific subject(s) data, please specify that by selecting the Choose subjects button and choosing your subjects.

## <a name="run"></a> Running the Subject File Crawler

Once you have specified all of the parameters as you desire, click the 'Start' button on the bottom of the GUI to start the process.  

A success popup will appear when the process is completed.
