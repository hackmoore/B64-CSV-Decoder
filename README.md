# B64-CSV-Decoder
A small script to decode Base64 cells in a CSV and output them as files.

## Requirements
- Python3
- openpyxl library (`pip3 install openpyxl`)

## Notes
There is no definitive way to know if a string is Base64 encoded or just *might* be so it takes it's best guess. Some output files might be garbage.

## Usage
### `-f`|`--file`
**REQUIRED**
The CSV *file* that the script should attempt to open.

### `-o`|`--output`
**REQUIRED**
The *directory* that the script should output files to

### `-e`|`--ext`
**OPTIONAL**
The extension you would like to append to output files (default is none)

### `--row`
**OPTIONAL**
Instructs the script to only look at a single row rather than all rows

### `--col`
**OPTIONAL**
Instructs the script to only look at a single column rather than all columns

### `-l`|`--log`
**OPTIONAL**
The location to write the output log to

### `-u`|`--update`
**OPTIONAL**
If flagged, will overwrite existing output files

### `-v`|`--verbose`
**OPTIONAL**
Print out additional information to the console/logs.
