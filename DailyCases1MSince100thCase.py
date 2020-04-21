
import csv


COUNTRY_KEY = 'Country or Area'
POP_KEY = 'Value'
YEAR_KEY = 'Year(s)'


C100_COUNTRY_KEY = 'Entity'
C100_DATE_KEY = 'Date'
C100_CASES_KEY = ' (cases)'
C100_DAYS_SINCE_100 = 'Days since the 100th confirmed case (days)'
C100_CASES_NORMALIZED_BY_POP = '(cases/1M)'

STATS_TO_POPULATION_COUNTRY_MAPPING = {
    'United States' : 'United States of America',
    'Asia excl. China' : '',
    'Bolivia' : 'Bolivia (Plurinational State of)',
    'Bonaire Sint Eustatius and Saba' : 'Bonaire, Sint Eustatius and Saba',
    'Brunei' : 'Brunei Darussalam',
    'Cape Verde' : 'Cabo Verde'
    }

with open('covid-confirmed-cases-since-100th-case.csv') as c100csv, open('UNdata_Export_20200421_033001429.csv') as populationByCountry, open('output.txt', 'w') as output:
    c100 = csv.DictReader(c100csv)
    population = csv.DictReader(populationByCountry)
    populationDict = {}
    for row in population:
        assert(row[YEAR_KEY] == '2019')
        populationDict[row[COUNTRY_KEY]] = float(row[POP_KEY]) / 1000
    skipped = set()

    for row in c100:
        country = row[C100_COUNTRY_KEY]

        populationCountryKey = country

        if country not in populationDict:
            if country not in STATS_TO_POPULATION_COUNTRY_MAPPING:
                skipped.add(country)
                continue
            populationCountryKey = STATS_TO_POPULATION_COUNTRY_MAPPING[country]

        if populationCountryKey not in populationDict:
            skipped.add(country)
            continue

        casesCount = 0
        if row[C100_CASES_KEY] != '':
            casesCount = row[C100_CASES_KEY]

        print('%s, %s, %s, %f, %s' % (country, 
                                  row[C100_DATE_KEY],
                                  casesCount, 
                                  int(casesCount) / populationDict[populationCountryKey],
                                  row[C100_DAYS_SINCE_100]), file=output)

    print(str(skipped))