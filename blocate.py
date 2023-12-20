#!/usr/bin/python3

import os
import subprocess as sub
import sys
import argparse as ap


args = sys.argv

#
#   build argparser
#

# consider support for these other cool options:
#https://phoenixnap.com/kb/locate-command-in-linux

aparse = ap.ArgumentParser(prog='blocate.py',
            description='A more powerful version of locate command',
            epilog='')

aparse.add_argument('searchTerms', metavar='term', type=str,nargs='+',
                    help="A search term. Multiple terms are AND'ed together")

aparse.add_argument('-v', metavar='term', type=str,nargs='+',
                    help='Eliminate the next search term from results (grep -v)')

aparse.add_argument('--Case',  dest='case', action='store_true',
                    help="Be case sensitive (default not case sensitive)")

aparse.add_argument('--home',  dest='home', action='store_true',
                    help="Automatically limit the search to the user's home dir")

aparse.add_argument('--cmd',  dest='cmd', action='store_true',
                    help="Print the command line generated for the search")

aparse.add_argument('--update',  dest='update', action='store_true',
                    help="Update the locate database (requires password).")

aparse.add_argument('--dirs',  dest='dirs', action='store_true',
                    help='Only print directories which match or have matching files (but not the files)')


#
#   Pre-process the arg list to hide the -v options(!)#_#_(__
#
flipnext = False
newargs = []
prefix = '**NNNNNNNNNNN**' # note this precludes certain search terms!!
for a in sys.argv:
    if flipnext:
        if a == '-v':
            print('Command Line error:  no "-v -v"!')
            quit()
        newargs.append(prefix+a)  # to be flipped with 'grep -v arg'
        flipnext=False
    elif a == '-v':
        flipnext = True
    else:
        newargs.append(a)  # non flipped: 'grep arg'

#
#   work on the arguments
#

args = aparse.parse_args(newargs)

#print('Args: ', args)

args.searchTerms = args.searchTerms[1:]  # drop program name
#
#  update DB if asked
#
if args.update:
    tmp = sub.check_output('sudo updatedb',shell=True)
    if len(args.searchTerms) == 0:
        quit()
#
#  process -v modifiers
#

negNext = False
grepTerms = []
for term in args.searchTerms:
    if negNext:
        grepTerms.append('-v '+term)
        negNext = False
    if term == '-v':
        negNext = True
    else:
        grepTerms.append(term)


homedir = 'unknown'
if args.home:
    homedir = str(sub.check_output('echo $HOME',shell=True)[:-1].decode('UTF-8'))


#print("Home: ",homedir)
#print("Search Term(s)")
#print(args.searchTerm)

if args.case:
    cmd = 'locate '
else:  # default is case insensitive
    cmd = 'locate -i '

i=0
for a in grepTerms:
        if a.startswith(prefix):   # restore the -v option modifer for grep
            a = '-v '+ a[len(prefix):]
        if i==0:
            cmd += a
        else:
            cmd += f'| grep {a} '
        i+=1
        #print(f'{i:3} {a}')


if homedir != 'unknown':
    cmd += f'| grep {homedir}  '

if args.cmd:
    print("Command: ",cmd)

#rawres = sub.check_output(cmd,shell=True)
try:
    rawres = sub.check_output(cmd,shell=True)
except sub.CalledProcessError as grepexc:
    print("Sorry, there were no results")
    quit()
# Parse the output as a list of strings
lines = rawres.decode("utf-8").splitlines()

i=0
prevline = 'aldjflawe8203498ijcmk'
dirs = []

if not args.dirs:
    print("All Results:")
    for l in lines:
        i+=1
        print(f'{i:3}  {l}')
else:
    # scan for the dirs
    for l in lines:
        if l.startswith(prevline+'/'):
            dirs.append(prevline+'/')
        prevline = l
    i=0

    if len(lines) == 0:
        print('there were no matches')
        quit()

    for l in lines:
        if l[0] == '/':  # get rid of leading /
            l = l[1:]
        parts = l.split('/')
        candidate = '/'
        for p in parts[:-1]:
            candidate += p + '/'
        dirs.append(candidate)
    # deduplicate
    dirs = list(set(dirs))

    print ('Directory Results: ')
    # print them
    for d in dirs:
        i+=1
        print(f'{i:3}  {d}')




