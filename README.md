time-worked
===========

A few python scripts for logging how much time I've worked on some project.

They run under Python 2.7.

# Using the scripts
Run `startTime.py` to log the starting of your work on a project, and `stopTime.py` to log the ending of a time segment.  These scripts will log the time in a `Time Worked.txt` file.

Run `totalTime.py` to see how much time you've worked so far, as logged in the `Time Worked.txt` file.

Run `splitTime.py` to split off all of your current time into a separate file, and start with a fresh `Time Worked.txt` file.  The separate file will have, at the bottom, a log of the total time in that file.

Run `totalTimeAllFiles.py` to see how much time you've worked so far, as logged in `Time Worked.txt` and any other files made by `splitTime.py`.

Run `pastWeekTime.py` or `pastWeekTimeAllFiles.py` to see the time you've worked in the past week, segmented by day.