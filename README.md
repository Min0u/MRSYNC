```MRsync

NAME
       mrsync - minimalistic version of rsync

SYNOPSIS
mrsync.py [OPTION]... SRC [SRC]... DEST

 mrsync.py [OPTION]... SRC [SRC]... [USER@]HOST:DEST

mrsync.py [OPTION]... SRC

mrsync.py [OPTION]... [USER@]HOST:SRC [DEST]

DESCRIPTION
       mrsync is a program that behaves in much the same way that rsync does, but
       has less options. 

GENERAL
       mrsync copies files either to or from a remote host, or locally  on  the
       current  host  (it  does  not  support copying files between two remote
       hosts).

       There are two different ways for mrsync  to  contact  a  remote  system:
       using  ssh.    
       The remote-shell  transport is used whenever the source or destination path 
       contains a single colon (:) separator after a host specification.
       
       As a special case, if a single source arg is specified without a desti-
       nation, the files are listed in an output format similar to "ls -l".

       As expected, if neither the source or destination path specify a remote
       host, the copy occurs locally (see also the --list-only option).


SETUP
       First download the zip to your local machine, then extract them.

       Once  installed,  you  can use mrsync to any machine that you can access
       via a remote shell (as well as some that you can access using the mrsync
       daemon-mode  protocol).   

       Note  that  mrsync  must be installed on both the source and destination
       machines.


USAGE
       You use mrsync in the same way you use rcp. You must  specify  a  source
       and a destination, one of which may be remote.

       Perhaps the best way to explain the syntax is with some examples:

       When using mrsync, the -r option allows you to copy directories recursively. 
       To use it, you must specify a source and a destination, one of which may be remote.

       mrsync -r foo:src/ /data/tmp/

       This would copy the contents of the remote directory src on the machine foo into the 
       local directory /data/tmp/. The trailing slash on the source directory is important, 
       as it tells mrsync to copy the contents of the directory, rather than the directory itself.

       mrsync -r /data/documents/ bar:backup/

       This command would recursively copy the entire documents directory and all of its contents 
       from the local machine to the backup directory on the remote machine bar.

       When using the -r option, mrsync will copy the entire directory tree, preserving all of the 
       subdirectories and files. 
       
       You can also use mrsync in local-only mode, where both the source and destination do not 
       contain a : in the name. In this case, mrsync behaves like an improved copy command, 
       allowing you to easily copy directories and their contents.

OPTIONS SUMMARY
       Here is a short summary of the options available in mrsync. Please refer
       to the detailed description below for a complete description.

        -v, --verbose               increase verbosity
        -q, --quiet                 suppress non-error messages
        -r, --recursive             recurse into directories
        -u, --update                skip files that are newer on the receiver
        -d, --dirs                  transfer directories without recursing
            --delete                delete extraneous files from dest dirs
            --force                 force deletion of dirs even if not empty
            --size-only             skip files that match in size
            --list-only             list the files instead of copying them
       -h   --help                  show this help


OPTIONS
       Many  of  the  command  line options  have  two  variants,  one short and 
       one long.  These are shown below, separated by commas. Some options only 
       have a long variant.  The '='  for  options  that take a parameter is 
       optional; whitespace can be used instead.


       --help Print a short help page  describing  the  options  available  in
              mrsync  and exit.  For backward-compatibility with older versions
              of mrsync, the help will also be output if you use the -h  option
              without any other args.

       -v, --verbose
              This  option  increases  the amount of information you are given
              during the transfer.  By default, mrsync works silently. A single
              -v  will  give you information about what files are being trans-
              ferred and a brief summary at the end. Two -v  flags  will  give
              you  information  on  what  files are being skipped and slightly
              more information at the end. More than two -v flags should  only
              be used if you are debugging mrsync.

              Note that the names of the transferred files that are output are
              just  the  name of the file. At the single -v level of verbosity, 
              this does not mention when a file gets its attributes changed.             

       -q, --quiet
              This  option  decreases  the amount of information you are given
              during the transfer, notably  suppressing  information  messages
              from  the remote server. This flag is useful when invoking mrsync
              from cron.

       --size-only
              Normally mrsync will not transfer any files that are already  the
              same  size  and  have the same modification time-stamp. With the
              --size-only option, files will not be transferred if  they  have
              the  same  size,  regardless  of  timestamp. This is useful when
              starting to use mrsync after using another mirroring system which
              may not preserve timestamps exactly.

     

 
       -r, --recursive
              This  tells  mrsync  to  copy  directories recursively.  See also
              --dirs (-d).

       -u, --update
              This  forces mrsync to skip any files which exist on the destina-
              tion and have a modified time that  is  newer  than  the  source
              file.   (If an existing destination file has a modify time equal
              to the source file's, it will be updated if the sizes  are  dif-
              ferent.)


       -d, --dirs
              Tell the sending  side  to  include  any  directories  that  are
              encountered.  Unlike --recursive, a directory's contents are not
              copied unless the directory name specified is "." or ends with a
              trailing  slash (e.g. ".", "dir/.", "dir/", etc.).  Without this
              option or the --recursive option, mrsync will skip  all  directo-
              ries it encounters (and output a message to that effect for each
              one).  If you specify both --dirs and  --recursive,  --recursive
              takes precedence.

       --delete
              This  tells  mrsync to delete extraneous files from the receiving
              side (ones that aren't on the sending side), but  only  for  the
              directories  that  are  being synchronized.  You must have asked
              mrsync to send the whole directory (e.g. "dir" or "dir/") without
              using  a  wildcard  for  the directory's contents (e.g. "dir/*")
              since the wildcard is expanded by the shell and mrsync thus  gets
              a  request  to  transfer individual files, not the files' parent
              directory.  

              This option has no effect unless either --recursive or --dirs 
              (-d) is set, but only for  directories whose contents are being copied.

       --force
              This  option tells mrsync to delete a non-empty directory when it
              is to be replaced by a non-directory.  This is only relevant  if
              deletions are not active (see --delete for details).

       --list-only
              This  option will cause the source files to be listed instead of
              transferred.  This option is  inferred  if  there  is  a  single
              source  arg  and no destination specified, so its main uses are:
              (1) to turn a copy command that includes a destination arg  into
              a  file-listing command, (2) to be able to specify more than one
              local source arg (note: be sure to include the destination).
     
BUGS/KNOWN ISSUES
Due to recent changes, the file updates do not work. Other cases may not work properly
-Incremental transfer: 
We managed to implement functions to make it work (cf. checksums.py) but several problems were encountered after its integration in the modules (as generator).
We decided to restore the old version without its implementation. We only used the md5 hash (no Adler32).
      
-Ssh:
 After some modifications, updating file in pull/push don't work anymore. 

-Daemon mode:
 Not functional: the prototype is in demon.py but is not used by the other modules


INTERNAL OPTIONS
       The option --server is used  internally  by  mrsync,  and
       should  never  be  typed  by  a  user under normal circumstances.


AUTHORS
       This mrsync has been written by   Min0u
                                         Obludaaa

                                  L2 Info, Math-Info 2023             mrsync(1)














