__author__ = 'Laura'


import csv
import numpy as np
from datetime import datetime


def convert_to_datetime(sometime):
    return datetime.strptime(sometime, '%Y-%m-%dT%H:%M:%S.%fZ')


class Walk(object):
    """
    Parses csv export from Google My Tracks program, and pulls out heart rate information

    Attributes:
        name: name of the file as given, no extension
        activity: physical activity associated with file (e.g. walking, biking, running)
        description: any description provided by the user in at the time file was written
        hr: heart rate data, as a numpy float array
        time: datetime object containing an array of recorded point times
    """
    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name, 'rb') as f:
            reader = csv.reader(f)
            reader.next()  # skips first line
            line = reader.next()
            self.name = line[0]
            self.activity = line[1]
            self.description = line[2]
            reader.next()  # skips blank line
            headers = reader.next()
            hr_index = headers.index('Heart rate (bpm)')
            time_index = headers.index('Time')
            self.hr = []
            self.time = []
            for line in reader:
                try:
                    # might change error-checking in heart rate values here
                    if not (line[hr_index] == '' or line[hr_index] == '-1.0'):
                        self.hr.append(line[hr_index])
                    self.time.append(convert_to_datetime(line[time_index]))
                except IndexError:
                    break
            self.hr = np.array(self.hr, dtype=float)
    def __str__(self):
        return ' - '.join([self.name, self.activity, self.description])
