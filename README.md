# Intro

Hey there. This is a short script I use to create a convenient workflow mark CSSE2002 assignments. I'm not sure how other tutors mark their assignments so this might or might not be suitable for you.

# How to use

Clone this repo and run 

```bash
$ python3.9 open_script.py -h
usage: open_script.py [-h] [-d DONE] [--ide [IDE]] [-m]
                      [-i [IGNORE_MERGE [IGNORE_MERGE ...]]] [-c]
                      bundle

positional arguments:
  bundle

optional arguments:
  -h, --help            show this help message and exit
  -d DONE, --done DONE  Number of already marked assignments
  --ide [IDE]           IDE to be opened, has to be in $PATH
  -m, --merge           Merge mode, all student's files will be accumulated
                        into a single file called merged.java and that file
                        will be opened.
  -i [IGNORE_MERGE [IGNORE_MERGE ...]], --ignore-merge [IGNORE_MERGE [IGNORE_MERGE ...]]
                        Ignore specified files while merging, useful to leave
                        out provided code
  -c, --confirm-continue
                        Program will ask for your confirmation before moving
                        on to next student
```

to see all the options. Normally you just need to provide the bundle directory for this to work.

This script will loop through all the assignments in the bundle directory and open each of them in your IDE. After finishing marking an assignment, the next one will be opened.

 If you have marked N assignments, specify the `-d` or `--done` option. `--ide` is your editor of choice, by default this is set to `code`, but you can use for instance `subl` or `atom`, remember to install the shell command beforehand if needed. Vim doesn't work sorry vim nerdies :(. If you want the script to ask for your confirmation before moving on to the next assignment, specify `-c`.

Happy marking (heh).