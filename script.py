#!/usr/bin/env python

import argparse
import logging
import csv
import base64
from os import makedirs, path
from openpyxl.utils import get_column_letter





def isBase64(s):
    # A basic check first
    if len(s) % 4 != 0: return False

    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def xlref(row, column, zero_indexed=True):
    if zero_indexed:
        row += 1
        column += 1
    return get_column_letter(column) + str(row)

def writeLog(text, level='INFO'):
    if(getattr(logging, level) >= LOG_LEVEL):
        print(text)
        if(args.log is not None):
            getattr(logging, level.lower())(text)



if __name__ == '__main__':
    # Check the arguments
    args = argparse.ArgumentParser()
    args.add_argument("-f", "--file", required=True, help="The CSV file to load.")
    args.add_argument("--col", required=False, help="A specific column to run over (default: all cols).")
    args.add_argument("--row", required=False, help="A specific row to run over (default: all rows).")
    args.add_argument("-o", "--output", required=True, help="Directory to output files to.")
    args.add_argument("-e", "--ext", required=False, help="Extension to write files to (default: none).")
    args.add_argument("-l", "--log", required=False, help="Location of log file (default: none).")
    args.add_argument("-u", "--update", required=False, action="store_true", help="Write over existing files.")
    args.add_argument("-v", "--verbose", required=False, action="store_true", help="Print verbosely to the logs and screen.")
    args = args.parse_args()

    # Check for a valid input file
    if not path.isfile(args.file):
        print("CSV file does not exist")
        exit(1)

    # Create the output dir if required
    if not path.exists(args.output):
        makedirs(args.output)

    # Open the log file
    LOG_LEVEL = 10 if args.verbose else 40
    if args.log is not None and args.log != "":
        logging.basicConfig(filename=args.log, level=LOG_LEVEL, datefmt='%y-%m-%d %H:%M:%S')

    # Open the CSV
    with open(args.file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 1

        for row in csv_reader:
            # Skip if it's not the row we're searching for
            if args.row is not None and row_count != int(args.row):
                writeLog("Skipping row(%d)"%row_count, 'DEBUG')
                row_count += 1
                continue

            # Parse through the row
            col_count = 1
            for cell in row:
                # Skip the column if it's not what we're looking for
                if args.col is not None and col_count != int(args.col):
                    writeLog("Skipping col(%d)"%col_count, 'DEBUG')
                    col_count += 1
                    continue

                # Check for valid BASE64 code
                cell = str.encode(cell)
                if isBase64(cell):
                    outpath = args.output.rstrip('/') + '/' + xlref(row_count, col_count) + ('.'+args.ext if args.ext else '')
                    writeLog("(%s, %s) is B64"%(row_count, col_count), 'INFO')
                    if not path.isfile(outpath) or (path.isfile(outpath) and args.update == True):
                        writeLog("(%s, %s) Updating file %s" % (row_count, col_count, outpath), 'INFO')
                        with open(outpath, 'wb') as outfile:
                            outfile.write(base64.b64decode(cell))
                    else:
                        writeLog("(%s, %s) Skipping existing file (%s)" %(row_count, col_count, outpath), 'INFO')

                else:
                    writeLog("(%s, %s) not B64"%(row_count, col_count), 'DEBUG')

                col_count += 1

            # Move to the next row
            row_count += 1

    writeLog("Fin.")