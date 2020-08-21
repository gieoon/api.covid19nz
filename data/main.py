# https://nzcoviddashboard.esr.cri.nz/#!/

# https://www.stats.govt.nz/experimental/covid-19-data-portal

# http://api.covid19live.com/data/processed/timeseries.min.json

# Processing the CSV files to construct timeseries.json & data.json
# Save all of this data into DB

# Separately scrape or update the site on a daily basis.
import pandas as pd
import datetime
from datetime import timedelta
import json

tested_df = pd.read_csv('./tests_per_dhb.csv')
# print(tested_df.head(10))

def getTestedCount(region):
    if region == 'Midcentral':
        region = 'Mid Central'
    if region == 'Tairawhiti':
        region = 'Tairāwhiti'
    if region == 'Waitemata':
        region = 'Waitematā'
    # print(region,tested_df.loc[tested_df['DHB'] == region]['Total tested'])
    return int(tested_df.loc[tested_df['DHB'] == region]['Total tested'].values[0])


# df = pd.read_csv('./covid_19_data_portal.csv')
# df = pd.read_csv('./covid-cases-Confirmed.csv')
# df = pd.read_csv('./jhhs_confirmed.csv')
df = pd.read_csv('timeseries_dhb.csv')
# print(df.head(10))
# print(df.columns)
timeseries = {}
def createDatesForDHB(df):
    # print(df['Region'].values[0])
    region = df['Region'].values[0]
    if region == 'New Zealand':
        return

    timeseries[region] = {
        "dates": {}
    }
    for index, row in df.iterrows():
        # print(date)
        date = row['Date']
        timeseries[region]['dates'][date] = {
            "delta": {
                "confirmed": row['Daily confirmed'],
                "probable": row['Daily probable'],
                "recovered": row['Daily total cases'] - row['Daily deceased'] - row['Daily probable'],
                "deceased": row['Daily deceased'],
                "total": row['Daily total cases'],
                "tested": getTestedCount(region)
            },
            "total": {
                "confirmed": row['Cumulative confirmed'],
                "probable": row['Cumulative probable'],
                "recovered": row['Cumulative total cases'] - row['Cumulative deceased'] -row['Cumulative probable'],
                "deceased": row['Cumulative deceased'],
                "total": row['Cumulative total cases'],
                "tested": getTestedCount(region) # Need to pull this data from worldometers
            }
        }

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
# df['Date'] = df['Date'] + timedelta(days=5)
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# pd.DatetimeIndex(df['Date']) + pd.DateOffset(2)

# print(df.tail(10))

# Group dataframe into regions
for i, g in df.groupby('Region'):
    createDatesForDHB(g)

# print(df['Region'].unique())
# Extract all historical data as timeseries data

# Create timeseries for whole of NZ from John Hopkins data
confirmed_df = pd.read_csv('./jhhs_nz_confirmed.csv')
recovered_df = pd.read_csv('./jhhs_nz_recovered.csv')
deaths_df = pd.read_csv('./jhhs_nz_recovered.csv')

# Extract NZ row because this data has all of the countries
def getNZRow(df):
    return df.loc[df['Country/Region'] == 'New Zealand']

# print(confirmed_df.columns[4:])
timeseries['TT'] = {
    'dates': {}
}
previousConfirmed = 0
previousRecovered = 0
previousDeceased = 0
previousTested = 0



for date in confirmed_df.columns[4:]:
    confirmed = int(getNZRow(confirmed_df)[date].values[0])
    recovered = int(getNZRow(recovered_df)[date].values[0])
    deceased = int(getNZRow(deaths_df)[date].values[0])
    tested = getTestedCount('TT') # Need to pull this data from worldometers
    # print(confirmed_df[date].values)
    timeseries['TT']['dates'][date] = {
        "delta": {
            "confirmed": confirmed - previousConfirmed,
            "probable": 0,
            "recovered": recovered - previousRecovered,
            "deceased": deceased - previousDeceased,
            "total": 0,
            "tested": tested - previousTested
        },
        "total": {
            "confirmed": confirmed,
            "probable": 0,
            "recovered": recovered,
            "deceased": deceased,
            "total": confirmed + recovered + deceased,
            "tested": tested
        }
    }
    previousConfirmed = confirmed
    previousRecovered = recovered
    previousDeceased = deceased
    previousTested = tested

# print(timeseries['TT'])
# Construct output JSON
with open('./processed/timeseries.min.json', 'w', encoding='utf-8') as f:
    json.dump(timeseries, f, ensure_ascii=False, indent=4)

# Construct data.json, which holds current figures for each region.
data = {}

population_df = pd.read_csv('./dhb_populations.csv')

def getPopulation(region):
    # print(region)
    if region == 'Mid Central':
        region = 'Midcentral'
    if region == 'Tairāwhiti':
        region = 'Tairawhiti'
    if region == 'Waitematā':
        region = 'Waitemata'
    # print(population_df.loc[population_df['Region'] == region])
    return int(population_df.loc[population_df['Region'] == region]['Population'].values[0])

today_df = pd.read_csv('./overview_today.csv')


daily_df = pd.read_csv('./overview_daily.csv')
# print(daily_df.head(5))

# Join today & daily on Region
today_df = pd.merge(today_df, daily_df, on='Region', how='inner') #suffixes='df1', 'df2'
# print(today_df.head(5))
# Set the previous to the second to last column in timeseries data
# previousConfirmed = int(confirmed_df.columns[-2].values[0])
# previousDeceased = int(deaths_df[-2].values[0])
# previousRecovered = int(recovered_df[-2].values[0])

previousConfirmed = 0
previousDeceased = 0
previousRecovered = 0

print(list(timeseries['TT']['dates'].keys())[-2])

lastDate = list(timeseries['TT']['dates'].keys())[-2]
print(int(confirmed_df[lastDate].values[0]), int(deaths_df[lastDate].values[0]), int(recovered_df[lastDate].values[0]))

for index, row in today_df.iterrows():
    region = row['Region']
    if region == 'New Zealand':
        region = 'TT'
    # print(getPopulation(region),": ",getTestedCount(region))
    data[region] = {
        "delta": {
            "confirmed": row['Confirmed'] + row['Probable'] - int(confirmed_df[lastDate].values[0]),
            "deceased": row['Deceased'] - int(deaths_df[lastDate].values[0]),
            "recovered": row['Recovered'] - int(recovered_df[lastDate].values[0]),
        },
        "meta": {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+12:00"),#"2020-08-16T22:17:52+05:30",
            "population": getPopulation(region),
            "tested": {
                # Update from URL, needs to be passed in or scraped with each scrape.
                "last_updated": "2020-08-10",
                #datetime.datetime.now().strftime("%Y-%m-%d"),#"2020-08-13",
                "source": "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-testing-rates-ethnicity-and-dhb"
            } 
        },
        "total": {
            "confirmed": row['Confirmed'] + row['Probable'],
            "active": row['Active'],
            "deceased": row['Deceased'],
            "recovered": row['Recovered'],
            "probable": row['Probable'],
            "tested": getTestedCount(region),
            "Incidence rate (per 100 000)":  row['Incidence rate (per 100 000)']
        }
    }
    # print(data[region])

# print(data)
with open('./processed/days/data.min.json', 'w', encoding='utf-8') as d:
    json.dump(data, d, ensure_ascii=False, indent=4)

# Append update.json contents to updates_previous.json
# updates = []
# with open('./updates.json', 'w') as updates:
#     with open('./updates_previous.json', 'w') as previous:



'''
1. Create the dataset
2. Save the dataset to the DB
3. Rewire API call to load the data in the same format into timeseries.
4. Automate new data using Github Actions

'''

