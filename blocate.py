#!$/usr/bin/python3

import os
import subprocess as sub
import sys
import argparse as ap


args = sys.argv

#
#   build argparser
#

aparse = ap.ArgumentParser(prog='blocate.py',
            description='A more powerful version of locate command',
            epilog='')

aparse.add_argument('searchTerm', metavar='term', type=str,nargs='+',
                    help='A term to AND to with your search')
aparse.add_argument('--home',  dest='home', action='store_true',
                    help='automatically to limit search to users home dir')

aparse.add_argument('--dirs',  dest='dirs', action='store_true',
                    help='only print directories which match or have matching files (but not the files)')

args = aparse.parse_args()

homedir = 'unknown'
if args.home:
    homedir = str(sub.check_output('echo $HOME',shell=True)[:-1].decode('UTF-8'))

#print("Home: ",homedir)
#print("Search Term(s)")
#print(args.searchTerm)

cmd = 'locate '

i=0
for a in args.searchTerm:
        if i==0:
            cmd = f'locate {a} '
        else:
            cmd += f'| grep {a} '
        i+=1

if homedir != 'unknown':
    cmd += f'| grep {homedir}  '


#print("Command: ",cmd)

rawres = sub.check_output(cmd,shell=True)

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




