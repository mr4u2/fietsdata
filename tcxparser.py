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
        total = 0
        total_t = 0
        month = '{:02}'.format(month)
        for activity in self.root.Activities.Activity:
            activity_id = activity.Id
            # print(str(activity_id)[5:7])
            if str(activity_id)[5:7] == str(month) and str(activity_id)[0:4] == str(year):
                # laps = activity.findall(namespace + 'Lap')
                for lap in activity.Lap:
                    total += lap.DistanceMeters
                    total_t += lap.TotalTimeSeconds
        return { 'dist': total, 'time': total_t }

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
        total = 0
        total_time = 0
        month = '{:02}'.format(month)
        activities = self.parse_month(year, month)
        for activity in activities:
            laps = activity.findall(namespace + 'Lap')
            for lap in laps:
                total += lap.find(namespace + 'DistanceMeters')
                total_time += lap.find(namespace + 'TotalTimeSeconds')
        return {'dist': total, 'time': total_time / 3600}


def main():
    year_total = {}
    month_total = {}
    year_total_t = {}
    month_total_t = {}

    # Parse activities for each year, create totals for each month
    for year in range(START_YEAR, END_YEAR+1):
        fiets_info = TCXparser(PARSEFILE + str(year) + PARSEFILE2)
        year_tot = 0
        year_tot_t = 0
        month_total[year] = {}
        month_total_t[year] = {}
        for month in range(1, 13):
            month_all = fiets_info.total_month(year, month)
            month_tot = month_all['dist'] / 1000
            month_tot_t = month_all['time']
            # print('%02s : %10.2f' %(month, tot))
            year_tot += month_tot
            year_tot_t += month_tot_t
            month_total[year][month] = month_tot
            month_total_t[year][month] = month_tot_t
        year_total[year] = year_tot
        year_total_t[year] = year_tot_t
        # print('=== Year Total: %10.2f' %year_total)

    # Generate output distance
    grand_total = 0
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
                    print('%10.2f' % year_total[year], end='')
                    print('%10.2f' % year_total[year], end='', file=f)
                    grand_total += year_total[year]
                else:
                    print('%10.2f' % month_total[year][month], end='')
                    print('%10.2f' % month_total[year][month], end='', file=f)
            print()
            print(file=f)
        print('\nOverall distance: %5.2f km' % grand_total)
        print('\nOverall distance: %5.2f km' % grand_total, file=f)

        # Generate output time
        grand_total_t = 0
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
                    print('%10.2f' % year_total_t[year], end='')
                    print('%10.2f' % year_total_t[year], end='', file=f)
                    grand_total_t += year_total_t[year]
                else:
                    print('%10.2f' % month_total_t[year][month], end='')
                    print('%10.2f' % month_total_t[year][month], end='', file=f)
            print()
            print(file=f)
        print('\nOverall time: %5.2f hours' % grand_total_t)
        print('\nOverall time: %5.2f hours' % grand_total_t, file=f)

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
                    print('%10.2f' % (year_total[year] / year_total_t[year]), end='')
                    print('%10.2f' % (year_total[year] / year_total_t[year]), end='', file=f)
                else:
                    try:
                        print('%10.2f' % (month_total[year][month] / month_total_t[year][month]), end='')
                        print('%10.2f' % (month_total[year][month] / month_total_t[year][month]), end='', file=f)
                    except ZeroDivisionError:
                        print('%10s' % 'N/A', end='')
                        print('%10s' % 'N/A', end='', file=f)
            print()
            print(file=f)

        print('\nOverall average: %5.2f kph' % (grand_total / grand_total_t))
        print('\nOverall average: %5.2f kph' % (grand_total / grand_total_t), file=f)
        print('\n-----------------------------------------------------')
        print('\n-----------------------------------------------------', file=f)

if __name__ == '__main__':
    main()
