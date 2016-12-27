''' tcxparser.py, by Me, 2016-12-24
This class is used to parse TCX data files
'''

# import lxml
# import time
from lxml import objectify
# from lxml import etree
import calendar

namespace = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'

# PARSEFILE = 'F:\\fietsfiles\\18-12-2016 - 24-12-2016_history.tcx'
# PARSEFILE = 'F:\\fietsfiles\\2015_history.tcx'
PARSEFILE = 'F:\\fietsfiles\\'
PARSEFILE2 = '_history.tcx'
START_YEAR = 2012
END_YEAR = 2016


class TCXparser:
    def __init__(self, filename):
        self.file = filename
        try:
            self.tree = objectify.parse(filename)
            self.root = self.tree.getroot()

        except IOError as err:
            print('Error: {}'.format(err))

    def parse_activities(self):
        activity_ids = []
        for activity in self.root.Activities.Activity:
            activity_id = activity.Id
            print('%s' % activity_id)
            activity_ids.append(activity_id)

    def total_month_old(self, year, month):
        total_dist = 0
        total_time = 0
        total_num = 0
        month = '{:02}'.format(month)
        for activity in self.root.Activities.Activity:
            activity_id = activity.Id
            # print(str(activity_id)[5:7])
            if str(activity_id)[5:7] == str(month) and str(activity_id)[0:4] == str(year):
                total_num += 1
                # laps = activity.findall(namespace + 'Lap')
                for lap in activity.Lap:
                    total_dist += lap.DistanceMeters
                    total_time += lap.TotalTimeSeconds
        return { 'dist': total_dist, 'time': total_time, 'num': total_num }

    def parse_new(self):
        return self.root.Activities.xpath(".//Activity[@Sport='Biking']")

    def parse_new2(self):
        result = []
        for act in self.tree.iter('Activities'):
            print(act)
            result.append(act)
        return result

    def parse_new3(self):
        print('a--> ')
        a = self.root.getchildren()
        for i in a:
            print(i.getchildren())
        print('b--> ')
        b = a[0].getchildren()
        for i in b:
            print(i.getchildren())
        print('c--> ')
        c = b[0].getchildren()
        for i in c:
            print(i.getchildren())
        # for i in self.root.iterfind(".//*//Activities//Activity[@Sport='Biking']"):
        #     print(i)
        print('---+')
        results = [i for i in self.root.findall(namespace + 'Activities/' + namespace + 'Activity')]
        print(results)
        print(len(results))
        for Activity in results:
            print(str(Activity.findtext(namespace + 'Id'))[5:7])

    def parse_year(self, year):
        results = [i for i in self.root.findall(namespace + 'Activities/' + namespace + 'Activity') if str(i.findtext(namespace + 'Id'))[0:4] == str(year)]
        return results

    def parse_month(self, year, month):
        year_activities = self.parse_year(year)
        # results = [i for i in self.root.findall(namespace + 'Activities/' + namespace + 'Activity') if str(i.findtext(namespace + 'Id'))[5:7] == str(month)]
        results = [i for i in year_activities if str(i.findtext(namespace + 'Id'))[5:7] == str(month)]
        # print(results)
        return results

    def total_month(self, year, month):
        total_dist = 0
        total_time = 0
        total_num = 0
        month = '{:02}'.format(month)
        activities = self.parse_month(year, month)
        for activity in activities:
            total_num += 1
            laps = activity.findall(namespace + 'Lap')
            for lap in laps:
                total_dist += lap.find(namespace + 'DistanceMeters')
                total_time += lap.find(namespace + 'TotalTimeSeconds')
        return {'dist': total_dist, 'time': total_time / 3600, 'num': total_num}


def main():
    year_total_dist = {}
    month_total_dist = {}
    year_total_time = {}
    month_total_time = {}
    year_total_num = {}
    month_total_num = {}

    # Parse activities for each year, create totals for each month
    for year in range(START_YEAR, END_YEAR+1):
        fiets_info = TCXparser(PARSEFILE + str(year) + PARSEFILE2)
        year_tot_dist = 0
        year_tot_time = 0
        year_tot_num = 0
        month_total_dist[year] = {}
        month_total_time[year] = {}
        month_total_num[year] = {}
        for month in range(1, 13):
            month_all = fiets_info.total_month(year, month)
            month_tot_dist = month_all['dist'] / 1000
            month_tot_time = month_all['time']
            month_tot_num = month_all['num']

            # print('%02s : %10.2f' %(month, tot))
            year_tot_dist += month_tot_dist
            year_tot_time += month_tot_time
            year_tot_num += month_tot_num
            month_total_dist[year][month] = month_tot_dist
            month_total_time[year][month] = month_tot_time
            month_total_num[year][month] = month_tot_num
        year_total_dist[year] = year_tot_dist
        year_total_time[year] = year_tot_time
        year_total_num[year] = year_tot_num
        # print('=== Year Total: %10.2f' %year_total)

    # Generate output distance
    grand_total_dist = 0
    with open(PARSEFILE + 'Grand_total.txt', 'w') as f:
        for month in range(0, 14):
            if month == 0:
                print('--------------- Distance (km) -----------------------')
                print('--------------- Distance (km) -----------------------', file=f)
                print('   ', end='')
                print('   ', end='', file=f)
            elif month == 13:
                print('Tot', end='')
                print('Tot', end='', file=f)
            else:
                print(calendar.month_abbr[month], end='')
                print(calendar.month_abbr[month], end='', file=f)

            for year in range(START_YEAR, END_YEAR+1):
                if month == 0:
                    print('%10s' % year, end='')
                    print('%10s' % year, end='', file=f)
                elif month == 13:
                    print('%10.2f' % year_total_dist[year], end='')
                    print('%10.2f' % year_total_dist[year], end='', file=f)
                    grand_total_dist += year_total_dist[year]
                else:
                    print('%10.2f' % month_total_dist[year][month], end='')
                    print('%10.2f' % month_total_dist[year][month], end='', file=f)
            print()
            print(file=f)
        print('\nOverall distance: %5.2f km' % grand_total_dist)
        print('\nOverall distance: %5.2f km' % grand_total_dist, file=f)

        # Generate output time
        grand_total_time = 0
        for month in range(0, 14):
            if month == 0:
                print('\n--------------- Time (Hours) ------------------------')
                print('\n--------------- Time (Hours) ------------------------', file=f)
                print('   ', end='')
                print('   ', end='', file=f)
            elif month == 13:
                print('Tot', end='')
                print('Tot', end='', file=f)
            else:
                print(calendar.month_abbr[month], end='')
                print(calendar.month_abbr[month], end='', file=f)

            for year in range(START_YEAR, END_YEAR+1):
                if month == 0:
                    print('%10s' % year, end='')
                    print('%10s' % year, end='', file=f)
                elif month == 13:
                    print('%10.2f' % year_total_time[year], end='')
                    print('%10.2f' % year_total_time[year], end='', file=f)
                    grand_total_time += year_total_time[year]
                else:
                    print('%10.2f' % month_total_time[year][month], end='')
                    print('%10.2f' % month_total_time[year][month], end='', file=f)
            print()
            print(file=f)
        print('\nOverall time: %5.2f hours' % grand_total_time)
        print('\nOverall time: %5.2f hours' % grand_total_time, file=f)

        # Generate output average
        for month in range(0, 14):
            if month == 0:
                print('\n--------------- Averages (kph) ----------------------')
                print('\n--------------- Averages (kph) ----------------------', file=f)
                print('   ', end='')
                print('   ', end='', file=f)
            elif month == 13:
                print('Tot', end='')
                print('Tot', end='', file=f)
            else:
                print(calendar.month_abbr[month], end='')
                print(calendar.month_abbr[month], end='', file=f)

            for year in range(START_YEAR, END_YEAR+1):
                if month == 0:
                    print('%10s' % year, end='')
                    print('%10s' % year, end='', file=f)
                elif month == 13:
                    print('%10.2f' % (year_total_dist[year] / year_total_time[year]), end='')
                    print('%10.2f' % (year_total_dist[year] / year_total_time[year]), end='', file=f)
                else:
                    try:
                        print('%10.2f' % (month_total_dist[year][month] / month_total_time[year][month]), end='')
                        print('%10.2f' % (month_total_dist[year][month] / month_total_time[year][month]), end='', file=f)
                    except ZeroDivisionError:
                        print('%10s' % 'N/A', end='')
                        print('%10s' % 'N/A', end='', file=f)
            print()
            print(file=f)

        print('\nOverall average: %5.2f kph' % (grand_total_dist / grand_total_time))
        print('\nOverall average: %5.2f kph' % (grand_total_dist / grand_total_time), file=f)

        # Generate output number of rides
        grand_total_num = 0
        for month in range(0, 14):
            if month == 0:
                print('\n------------- Number of rides (avg distance) -----------------------')
                print('\n------------- Number of rides (avg distance) -----------------------', file=f)
                print('   ', end='')
                print('   ', end='', file=f)
            elif month == 13:
                print('Tot', end='')
                print('Tot', end='', file=f)
            else:
                print(calendar.month_abbr[month], end='')
                print(calendar.month_abbr[month], end='', file=f)

            for year in range(START_YEAR, END_YEAR+1):
                if month == 0:
                    print('%13s' % year, end='')
                    print('%13s' % year, end='', file=f)
                elif month == 13:
                    print('%4d - %6.2f' % (year_total_num[year], year_total_dist[year] / year_total_num[year]), end='')
                    print('%4d - %6.2f' % (year_total_num[year], year_total_dist[year] / year_total_num[year]), end='', file=f)
                    grand_total_num += year_total_num[year]
                else:
                    try:
                        print('%4d - %6.2f' % (month_total_num[year][month], month_total_dist[year][month] / month_total_num[year][month]), end='')
                        print('%4d - %6.2f' % (month_total_num[year][month], month_total_dist[year][month] / month_total_num[year][month]), end='', file=f)
                    except ZeroDivisionError:
                        print('%13s' % 'N/A', end='')
                        print('%13s' % 'N/A', end='', file=f)
            print()
            print(file=f)

        print('\nOverall number of rides: %4d Average distance: %5.2f km' % (grand_total_num, grand_total_dist / grand_total_num))
        print('\nOverall number of rides: %4d Average distance: %5.2f km' % (grand_total_num, grand_total_dist / grand_total_num), file=f)

        print('\n----------------- Totals ----------------------------')
        print('\n----------------- Totals ----------------------------', file=f)
        print('Number rides: %5d' % grand_total_num)
        print('Number rides: %5d' % grand_total_num, file=f)
        print('Distance:  %8.2f km' % grand_total_dist)
        print('Distance:  %8.2f km' % grand_total_dist, file=f)
        print('Time:      %8.2f hours' % grand_total_time)
        print('Time:      %8.2f hours' % grand_total_time, file=f)
        print('Avg distance: %5.2f km/per ride' % (grand_total_dist / grand_total_num))
        print('Avg distance: %5.2f km/per ride' % (grand_total_dist / grand_total_num), file=f)
        print('Avg time:     %5.2f h/per ride' % (grand_total_time / grand_total_num))
        print('Avg time:     %5.2f h/per ride' % (grand_total_time / grand_total_num), file=f)
        print('Avg speed:    %5.2f kph' % (grand_total_dist / grand_total_time))
        print('Avg speed:    %5.2f kph' % (grand_total_dist / grand_total_time), file=f)
        print('-----------------------------------------------------')
        print('-----------------------------------------------------', file=f)

if __name__ == '__main__':
    main()
