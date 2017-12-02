#!/usr/bin/env python3
"""
translate all csv files in the current directory from old to new `csv` format 
and put them into :path:`./translated/`
"""

import pdb
import os
import csv
import re
import datetime

ls = os.listdir()

for file in ls:

    print('file: ', file)

    protocol = []

    if file.endswith('.csv'):
        with open(file) as file:
            r = csv.reader(file, delimiter=';', quotechar='"')
            for line in r:
                if not line:
                    print('empty.')
                elif 'Datum' in line[0] or 'insgesamt' in line[0]:
                    print('omit ', line)
                else:
                    print('add ', line)
                    protocol.append(line)

        print('ready reading ', file.name)

        month = int(protocol[0][0].split(sep='.')[1])
        print('seems to be month %d' % month)

        year = int(file.name.split(sep='.')[1].split(sep='-')[0]) + 2000
        print('seems to be year %02d' % year)
        
        protocol_ng = []

        for line in protocol:
            print('processing %r' % line)
            date = line[0].split(sep='.')

            # comma transition
            try:
                idx = line[1].index(',')
                line[1] = line[1][:idx] + '.' + line[1][idx + 1:]
                print('change to %r' % line)
            except ValueError:
                print('unchanged')

            protocol_ng.append(['e', date[0], int(float(line[1]) * 3600), None, None, line[2]])

        print(protocol_ng)

        # fumble out fromto
        for row in protocol_ng:
            match = re.match('^[0-9:]{1,5}-[0-9:]{1,5}', row[5])
            if match:
                print('row contains fromto: %r' % row)

                # get day
                day = int(row[1])

                # get fromto
                fromto = match.group().split(sep='-')

                # get from 
                time = fromto[0].split(sep=':')
                from_hour = int(time[0])
                try:
                    from_minute = int(time[1])
                except IndexError:
                    from_minute = 0

                from_unixtime = int (datetime.datetime(year, month, day, from_hour, from_minute).timestamp())

                # get to
                time = fromto[1].split(sep=':')
                to_hour = int(time[0])
                try:
                    to_minute = int(time[1])
                except IndexError:
                    to_minute = 0
            
                to_unixtime = int (datetime.datetime(year, month, day, to_hour, to_minute).timestamp())

                print('extend row. with fromtime %02d:%02d (%d) totime %02d:%02d (%d) at %d-%02d' % (
                    from_hour, from_minute, from_unixtime, to_hour, to_minute, to_unixtime, year, month))

                row[3] = from_unixtime
                row[4] = to_unixtime

                print(row)

            else:
                print('no fromto found in %r' % row)
                

        try:
            os.mkdir('translated')
        except FileExistsError:
            pass

        with open('translated/%02d%02d.csv' % (year, month), 'w') as file:
            csv.writer(file).writerows(protocol_ng)
            
        

    


# vim: ai sts=4 ts=4 sw=4 expandtab
