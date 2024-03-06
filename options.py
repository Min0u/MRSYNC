import argparse, sys

def parse_arguments():
    # Création d'un parser
    parser = argparse.ArgumentParser(description='rsync')

    # Source
    parser.add_argument("source", action='append', help="the source file or directory", nargs='+')

    # Destination
    parser.add_argument("destination", help="the destination file or directory", nargs='?')

    # Options
    parser.add_argument('-r', '--recursive', action='store_true', help='Recurse into directories')
    parser.add_argument('--list-only', action='store_true', help='Only list files to be transferred')
    parser.add_argument('--delete', action='store_true', help='Delete extraneous files from destination directories')
    parser.add_argument('--force', action='store_true', help='Force deletion of directories even if not empty')
    parser.add_argument('-d','--dirs', action='store_true', help='Transfer directories without recursing')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('--server', action='store_true', help='Server mode')
    parser.add_argument('--size-only', action='store_true', help='Skip files that match in size')
    parser.add_argument('-u', '--update', action='store_true', help='Skip files that are newer on the receiver')
    #### PAS ENCORE IMPLEMENTE ####
    parser.add_argument('--whole-file', action='store_true', help='Transfer whole files')
    parser.add_argument('--checksum', action='store_true', help='Skip based on checksum, not mod-time & size')

    # Parsing de la ligne de commande
    args = parser.parse_args()

    if len(args.source[0]) < 1:
        if not args.quiet:
            print("Source obligatoire.")
        sys.exit(1)

    elif len(args.source[0]) > 1:
        args.destination = args.source[0][-1]
        args.source[0] = args.source[0][:-1]

    return args

helptext="""mrsync - minimalistic version of rsync.
rsync is a program that behaves in much the same way that rsync does, but has less options.

Usage: 
mrsync [OPTION]... SRC [SRC]... DEST
mrsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
mrsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
mrsync [OPTION]... SRC
mrsync [OPTION]... [USER@]HOST:SRC [DEST]
mrsync [OPTION]... [USER@]HOST::SRC [DEST]

The ':' usages connect via remote shell, while '::' & 'rsync://' usages connect to an rsync daemon, and require SRC or DEST to start with a module name.

Here is a short summary of the options available in rsync. Please refer to the detailed description below for a complete description.

-v, --verbose           increase verbosity
-q, --quiet             suppress non-error messages
-r, --recursive         recurse into directories
-u, --update            skip files that are newer on the receiver
-d, --dirs              transfer directories without recursing
    --delete            delete extraneous files from dest dirs
    --force             force deletion of dirs even if not empty
    --size-only         skip files that match in size
    --list-only         list the files instead of copying them
-h, --help              show this help
"""
