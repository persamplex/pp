
# pp is a simple git

this python code store you files and code with restore points, work on windows and linux

## --help

```bash
usage: pp.py [-h] [--install] [--version] [--backup [BACKUP]] [--point POINT] [--comment COMMENT]
             [--print-point [PRINT_POINT]] [--restore-point RESTORE_POINT] [--remove-point REMOVE_POINT] [--tag TAG]

IMPORTENT: Please use --install to make Bash Alias or Regestery for windows

options:
  -h, --help            show this help message and exit
  --install, -i         Install the alias for the script.
  --version, -v         Show the version of the script.
  --backup [BACKUP], -B [BACKUP]
                        Make a backup point from a file or directory
  --point POINT, -p POINT
                        Specify a file path to make point of the file
  --comment COMMENT, -c COMMENT
                        Textual content to comment (must be used with --point or --tag).
  --print-point [PRINT_POINT], -pr [PRINT_POINT]
                        Print points from datasheet (optional file name).
  --restore-point RESTORE_POINT, -re RESTORE_POINT
                        Restore file using the specified tag.
  --remove-point REMOVE_POINT, -rm REMOVE_POINT
                        Remove restore point using the specified tag.
  --tag TAG, -t TAG     using to specified a tag.
```
