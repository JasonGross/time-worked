#!/usr/bin/python
# TimeWorked.py
# Utility file to record working time
# Version 1.2, 2012-06-18
from __future__ import with_statement
from datetime import *
from time import *
import re, os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TIME_WORKED = os.path.join(SCRIPT_PATH, 'Time Worked.txt')
TIME_FORMAT = '%A, %B %d, %Y %H:%M.%S'

def parse_timedelta(duration):
    if 'day' in duration:
        if '.' in duration:
            duration = [int(j) for j in duration.replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
            duration = timedelta(duration[0], duration[3] + 60 * (duration[2] + 60 * duration[1]), duration[4])
        else:
            duration = [int(j) for j in duration.replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
            duration = timedelta(duration[0], duration[3] + 60 * (duration[2] + 60 * duration[1]), 0)
    else:
        if '.' in duration:
            duration = [int(j) for j in duration.replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
            duration = timedelta(0, duration[2] + 60 * (duration[1] + 60 * duration[0]), duration[3])
        else:
            duration = [int(j) for j in duration.replace('days', 'day').replace(' day, ',':').replace('.',':').split(':')]
            duration = timedelta(0, duration[2] + 60 * (duration[1] + 60 * duration[0]), 0)
    return duration


class TimeWorked(object):
    def __init__(self, begin=None, end=None, duration=None, fmt=TIME_FORMAT):
        if begin is None: begin = datetime.now()
        if isinstance(begin, str):
            self._parse(begin, fmt=fmt)
        elif isinstance(begin, TimeWorked):
            self._begin = begin.begin
            self._end = begin.end
            self._fmt = begin.time_format
            self._update_duration(begin.duration)
        else:
            self._begin = begin
            self._end = end
            self._fmt = fmt
            self._update_duration(duration)
    
    def _update_duration(self, duration=None):
        if duration is not None:
            if isinstance(duration, str): duration = parse_timedelta(duration)
            self._duration = duration
        elif self._begin is not None and self._end is not None:
            self._duration = self._end - self._begin
        else:
            self._duration = None

    def _get_begin(self): return self._begin
    def _get_end(self): return self._end
    def _get_duration(self): return self._duration
    def _get_format(self): return self._fmt
    
    def start(self, time=None):
        if time is None: time = datetime.now()
        self._begin = time
        self._update_duration()
            
    def stop(self, time=None):
        if time is None: time = datetime.now()
        self._end = time
        self._update_duration()

    begin = property(_get_begin, start)
    end = property(_get_end, stop)
    duration = property(_get_duration)
    time_format = property(_get_format)
        
    def _parse(self, log_entry, fmt=TIME_FORMAT):
        def parse_line_from_header(line, desc, header, strptime=(lambda time: datetime.strptime(time, fmt))):
            if line is not None:
                if line[:len(header)] != header:
                    raise Exception("Malformed log entry: %s should begin with '%s', not '%s'" %
                                    (desc, header, line[:len(header)]))
                return strptime(line[len(header):].strip())
            return None
        lines = [line.strip() for line in log_entry.split('\n') if line.strip()]
        if len(lines) == 0 or len(lines) > 3:
            raise Exception("Malformed log entry: there should be 1, 2, or 3 lines, not %s" % len(lines))
        begin = lines[0]
        end = lines[1] if len(lines) > 1 else None
        duration = lines[2] if len(lines) > 2 else None
        begin = parse_line_from_header(begin, 'the first line', 'Start: ')
        end = parse_line_from_header(end, 'the second line', 'End: ')
        duration = parse_line_from_header(duration, 'the third line', 'Time Spent: ', parse_timedelta)
        self.__init__(begin, end, duration, fmt)

    def parse(cls, log_entry, fmt=TIME_FORMAT):
        rtn = TimeWorked()
        rtn._parse(log_entry, fmt)
        return rtn

    parse = classmethod(parse)

    def parse_many(cls, log_entries, fmt=TIME_FORMAT):
        log_entries = [i.strip() for i in log_entries.split('\n\n') if 'Total Time:' not in i and i.strip()]
        return map(lambda log: TimeWorked.parse(log, fmt=fmt), log_entries)
    parse_many = classmethod(parse_many)

    def get_start_block(self):
        return "Start: " + self.begin.strftime(self.time_format)
    def get_end_block(self):
        return "End: %s\nTime Spent: %s" % (self.end.strftime(self.time_format), str(self.duration))
    start_block = property(get_start_block)
    end_block = property(get_end_block)
    def __str__(self):
        if self.end is None:
            return self.get_start_block()
        else:
            return self.get_start_block() + "\n" + self.get_end_block()
        
    def __repr__(self):
        return "TimeWorked(begin=%s, end=%s, duration=%s, fmt=%s)" % (repr(self.begin), repr(self.end), repr(self.duration), repr(self.time_format))

    def __add__(self, other):
        return self.duration + other
    def __radd__(self, other):
        return other + self.duration

def read_time_file(file_name=TIME_WORKED, print_error=True):
    try:
        with open(file_name, 'r') as f:
            lines = f.read()
    except Exception as e:
        if print_error:
            print(e)
            raw_input()
        raise e
    return read_time_log(lines, print_error=print_error)

def read_time_log(lines, print_error=False):
     return list(TimeWorked.parse_many(lines))
##    try:
##        times =
##        return times
##    except Exception as e:
##        if print_error:
##            print(e)
##            raw_input()
##        raise e

def write_begin_time(file_name=TIME_WORKED):
    #fmt = '\n'.join(['%' + i for i in 'aAbBcdHIjmMpSUwWxXyYZ%'])
    with open(file_name, 'a') as f:
        f.write(TimeWorked().start_block + '\n')

def write_end_time(file_name=TIME_WORKED, sleep_time=1):
    times = read_time_file(file_name)
    if times[-1].end is not None:
        print("No open time block.")
        raw_input()
        raise Exception("No open time block.")
    times[-1].stop()
    with open(file_name, 'a') as f:
        f.write(times[-1].end_block + '\n\n')
    print(times[-1].end_block)
    sleep(sleep_time)

def get_total_time(begin=None, end=None):
    return get_total_timef_between(TIME_WORKED, begin, end)

def get_total_timef_between(file_name, begin=None, end=None):
    def converter(time):
        if time.end is None:
            time = TimeWorked(time)
            time.stop()
        if begin is None or time.begin >= begin:
            if end is None or time.end <= end:
                return time
            elif time.begin <= end:
                return end - time.begin
        elif time.end >= begin:
            if end == None or time.end <= end:
                return time.end - begin
        return timedelta(0)
    return get_total_timef(file_name, converter)

def get_total_timef(file_name, converter=(lambda time: time)):
    times = read_time_file(file_name)
    return sum(map(converter, times), timedelta(0))
def get_total_time_files(file_list, begin=None, end=None):
    rtn = get_total_timef_between(file_list[0], begin, end)
    for i in file_list[1:]:
        rtn += get_total_timef_between(i, begin, end)
    return rtn

def get_total_time_by_day(get_time_method, begin=None, end=None):
    now = datetime.now()
    if begin is None and end is None:
        end_of_week_day = now.date() - timedelta(now.isoweekday()) # 1 is Monday
        beginning_of_week_day = end_of_week_day - timedelta(6)
        begin = beginning_of_week_day
        end = end_of_week_day
    if isinstance(end, date): end = datetime(end.year, end.month, end.day, 23, 59, 59, 999999)
    if isinstance(begin, date): begin = datetime(begin.year, begin.month, begin.day)
    rtn = {}
    while begin < end:
        begin = datetime(begin.year, begin.month, begin.day)
        cur_end = datetime(begin.year, begin.month, begin.day, 23, 59, 59, 999999)
        if cur_end > end: cur_end = end
        rtn[begin.date()] = get_time_method(begin, cur_end)
        begin += timedelta(1)
    return rtn

def get_total_time_by_day_files(file_list, begin=None, end=None):
    days = get_total_time_by_day((lambda begin, end: get_total_time_files(file_list, begin, end)), begin, end)
    rtn = ''
    for day in sorted(days.keys()):
        rtn += day.strftime('%a, %B %d, %Y') + ': ' + str(days[day]) + '\n'
    return rtn

def split_time():
    total = get_total_time()
    with open(TIME_WORKED, 'r') as f:
        lines = f.read()
    times = read_time_log(lines)
    begin = times[0].begin
    end = times[-1].end
    with open(os.path.join(SCRIPT_PATH, 'Time Worked (From ' + begin.strftime('%Y-%m-%d (%b)') + ' to ' + end.strftime('%Y-%m-%d (%b)') + ').txt'), 'w') as f:
        for i in times:
#            print(str(i))
            f.write(str(i) + '\n\n')
        f.write('\nTotal Time: ' + str(sum(times, timedelta(0))))
    with open(TIME_WORKED, 'w') as f:
        f.write('')
