#!/usr/local/bin/python2.7
# encoding: utf-8
'''
__main__ -- driver for MetroAppAnalysis

__main__ is a program to analyze Metro/Modern UI apps.

It defines classes_and_methods

@author:     @galenbwill @afrocheese

@copyright:  2015 Atredis Partners, LLC. All rights reserved.

@license:    Apache

@contact:    {galen,charles}@atredis.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from AppxMetadata import AppxMetadataParser

__all__ = []
__version__ = 0.1
__date__ = '2015-06-05'
__updated__ = '2015-06-05'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

WINDRIVE = 'C:\\'
if not os.path.ismount(WINDRIVE):
    WINDRIVE = ''
default_path = os.path.join(WINDRIVE, 'Program Files', 'WindowsApps')

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by @galenbwill @afrocheese on %s.
  Copyright 2015 Atredis Partners, LLC. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='*',
                            default=default_path)

        # Process arguments
        args = parser.parse_args()

        paths = args.paths if isinstance(args.paths, list) else [args.paths]
        verbose = args.verbose
        recurse = args.recurse
        inpat = args.include
        expat = args.exclude

        if verbose > 0:
            print("Verbose mode on")
            if recurse:
                print("Recursive mode on")
            else:
                print("Recursive mode off")

        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")

        if verbose > 0:
            print('paths: %s' % paths)

        def VLOG(msg, level=0):
            if verbose > level:
                print('LOG: %s' % msg)

        parser = AppxMetadataParser()
        for inpath in paths:
            if inpath == '-':
                VLOG("-")
                print(parser.parse(sys.stdin))
            elif os.path.isfile(inpath):
                VLOG("File: %s" % inpath)
                print(parser.parse(inpath))
            elif os.path.isdir(inpath):
                VLOG("Dir: %s" % inpath)
                visited = []
                for root, dirs, files in os.walk(inpath, followlinks=True):
                    VLOG("ROOT: %s" % root)
                    for file in files:
                        VLOG("FILE: %s" % os.path.join(root, file), 1)
                        if file == 'AppxManifest.xml':
#                             VLOG("APPX: %s" % os.path.join(root, file))
                            print(parser.parse(os.path.join(root, file)))
                            print('\tManifest: %s\n' % os.path.join(root, file))
            else:
                print >> sys.stderr, 'No such directory: ' + inpath

#         def process_poths(paths):
#             for inpath in paths:
#                 ### do something with inpath ###
#                 if verbose > 0:
#                     print(inpath)
#                 if os.path.exists(inpath):
#                     if os.path.isdir(inpath):
#                         pass
#                     else:
#                         pass
#                 else:
#                     print >> sys.stderr, 'No such directory: ' + inpath
#         process_paths(paths)
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
#     if DEBUG:
#         sys.argv.append("-h")
#         sys.argv.append("-v")
#         sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '__main___profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())