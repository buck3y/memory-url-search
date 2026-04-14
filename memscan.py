'''
Returns the URLS found in a large file
'''

import sys
import os
import re        # Python regular expression Library
import time

from prettytable import PrettyTable
from pathlib import Path

CHUNKSIZE = 65535
tbl = PrettyTable(["Occurrences", "URLS"])
tbl.title = "Sorted URL Results"
urlDict = {}

def chunkFile(largeFile):
    try:     
        with open(largeFile, 'rb') as targetFile:
            print("Processing file...")
            while True:
                fileChunk = targetFile.read(CHUNKSIZE)
                if fileChunk:  # if we still have data
                    urlRegex(fileChunk)
                else:
                    PrettyTable(tbl)
    except Exception as err:
        sys.exit("\nException: " + str(err) + " Script Aborted")
    print("\nFile Processed ... Script End")
def urlRegex(chunk):
    urlRegex = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w\.?=%&=\-@/$,]*')
    urlMatches = urlRegex.findall(chunk)
    for eachURL in urlMatches:
        try:
            # obtain the value if key exists and increment
            urlDict[eachURL] = urlDict.get(eachURL, 0) + 1
        except Exception:
            urlDict[eachURL] = 1     

def PrettyTable(table):
    print("\nGenerating Sorted Result Table")
    for url, urlCnt in urlDict.items():
        url_decoded = url.decode("utf-8")
        tbl.add_row([urlCnt, url_decoded])
    # Format output into pretty table
    tbl.align = 'l'
    print(tbl.get_string(sortby="Occurrences", reversesort=True))
    # Call HTML output function
    now = time.time()
    timeString = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime(now))
    htmlFileName = "WK-4-" + timeString + ".html"
    print("Saving results as an html file...")
    
    # Use the table passed as an argument
    htmlToSave = table.get_html_string(sortby="Occurrences", reversesort=True)
    
    with Path(htmlFileName).open(mode="w", encoding="utf-8") as fp:
        fp.write(htmlToSave)
        print("Saved file as", htmlFileName)

def Main():
    print("\nWK-4 : Myles Hurlbut - Version 1.3\n")
    while True:
        largeFile = input("Enter the name of a large File i.e d:/WK4/mem.raw >>> ")
        if os.path.isfile(largeFile):
            chunkFile(largeFile)
        else:
            print("Invalid file specified.")
            continue    
''' MAIN ENTRY POINT '''
if __name__ == '__main__':
    Main()
