# blocate
a better version of linux locate comand (actually a wrapper)

```
usage: blocate.py [-h] [-v term [term ...]] [--home] [--cmd] [--dirs] term [term ...]

A more powerful version of locate command

positional arguments:
  term                A search term. Multiple terms are AND'ed together

options:
  -h, --help          show this help message and exit
  -v term [term ...]  Eliminate the next search term from results (grep -v)
  --home              automatically limit the search to the user's home dir
  --cmd               print the command line generated for the search
  --dirs              only print directories which match or have matching files (but not the files)
```
