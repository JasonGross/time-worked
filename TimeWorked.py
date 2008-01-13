from __future__ import with_statement
from datetime import *
from time import *
import re
fmt = '%A, %B %d, %Y %H:%M.%S'
fname = 'Break Time.txt'
def write_begin_time():
    try:
        f = file(fname, 'r')
        lines = [i for i in f]
        f.close()
    except Exception:
        with file(fname, 'w') as f:
            lines = []
    #fmt = '\n'.join(['%' + i for i in 'aAbBcdHIjmMpSUwWxXyYZ%'])
    with file(fname, 'a') as f:
        f.write('Start: ' + datetime.now().strftime(fmt) + '\n')

def write_end_time():
    with file(fname, 'r') as f:
        lines = [i for i in f]
    start = datetime.strptime(lines[-1][len('Start: '):-1], fmt)
    with file(fname, 'a') as f:
        f.write('End: ' + datetime.now().strftime(fmt) + '\n')
        f.write('Time Spent: ' + str(datetime.now() - start) + '\n\n')

def get_total_time(begin=None, end=None):
    return get_total_timef(fname, begin, end)

def get_total_timef(file_name=None, begin=None, end=None):
    with file(file_name, 'r') as f:
        lines = [i for i in f]
    lines2 = []
    for i in range(len(lines)):
        if lines[i][:len('Time Spent: ')] == 'Time Spent: ':
            lines2.append([datetime.strptime(lines[i - 2][len('Start: '):-1], fmt), datetime.strptime(lines[i - 1][len('End: '):-1], fmt), lines[i][len('Time Spent: '):-1]])
    for i in lines2:
        if 'day' in i[-1]:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), i[-1][4])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), 0)
        else:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), i[-1][3])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), 0)
    total = timedelta(0)
    for i in lines2:
        if begin == None or i[0] >= begin:
            if end == None or i[1] <= end:
                total += i[-1]
            else:
                total += end - i[0]
        else:
            if end == None or i[1] <= end:
                total += begin - i[end]
    return total

def get_total_time_files(file_list, begin=None, end=None):
    rtn = get_total_timef(file_list[0], begin, end)
    for i in file_list[1:]:
        rtn += get_total_timef(i, begin, end)
    return rtn

def split_time():
    total = get_total_time()
    with file(fname, 'r') as f:
        lines = [i for i in f]
    lines2 = []
    for i in range(len(lines)):
        if lines[i][:len('Time Spent: ')] == 'Time Spent: ':
            lines2.append([datetime.strptime(lines[i - 2][len('Start: '):-1], fmt), datetime.strptime(lines[i - 1][len('End: '):-1], fmt), lines[i][len('Time Spent: '):-1]])
    for i in lines2:
        if 'day' in i[-1]:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), i[-1][4])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(i[-1][0], i[-1][3] + 60 * (i[-1][2] + 60 * i[-1][1]), 0)
        else:
            if '.' in i[-1]:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), i[-1][3])
            else:
                i[-1] = [int(j) for j in i[-1].replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
                i[-1] = timedelta(0, i[-1][2] + 60 * (i[-1][1] + 60 * i[-1][0]), 0)
    begin = lines2[0][0]
    end = lines2[-1][1]
    f = file('Time Spent (From ' + begin.strftime('%Y-%b-%d') + ' to ' + end.strftime('%Y-%b-%d') + ').txt', 'w')
    for i in lines:
        f.write(i)
    f.write('\nTotal Time: ' + str(total))
    f.close()
    f = file(fname, 'w')
    f.write('')
    f.close()
