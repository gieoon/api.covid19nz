# https://nzcoviddashboard.esr.cri.nz/#!/

# https://www.stats.govt.nz/experimental/covid-19-data-portal

# http://api.covid19live.com/data/processed/timeseries.min.json

# Processing the CSV files to construct timeseries.json & data.json
# Save all of this data into DB

# Separately scrape or update the site on a daily basis.
import pandas as pd
import datetime
import json

# df = pd.read_csv('./covid_19_data_portal.csv')
# df = pd.read_csv('./covid-cases-Confirmed.csv')
# df = pd.read_csv('./jhhs_confirmed.csv')
df = pd.read_csv('timeseries_dhb.csv')
print(df.head(10))
print(df.columns)
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
                "recovered": 0,
                "deceased": row['Daily deceased'],
                "total": row['Daily total cases'],
                "tested": 0
            },
            "total": {
                "confirmed": row['Cumulative confirmed'],
                "probable": row['Cumulative probable'],
                "recovered": 0,
                "deceased": row['Cumulative deceased'],
                "total": row['Cumulative total cases'],
                "tested": 0
            }
        }

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Group dataframe into regions
for i, g in df.groupby('Region'):
    createDatesForDHB(g)

# print(df['Region'].unique())
# Extract all historical data as timeseries data


# Create timeseries for whole of NZ from John Hopkins data
confirmed_df = pd.read_csv('./jhhs_nz_confirmed.csv')
recovered_df = pd.read_csv('./jhhs_nz_recovered.csv')
deaths_df = pd.read_csv('./jhhs_nz_recovered.csv')

# print(confirmed_df.columns[4:])
timeseries['TT'] = {
    'dates': {}
}
previousConfirmed = 0
previousRecovered = 0
previousDeceased = 0

for date in confirmed_df.columns[4:]:
    confirmed = int(confirmed_df[date].values[0])
    recovered = int(recovered_df[date].values[0])
    deceased = int(deaths_df[date].values[0])
    # print(confirmed_df[date].values)
    timeseries['TT']['dates'][date] = {
        "delta": {
            "confirmed": confirmed - previousConfirmed,
            "probable": 0,
            "recovered": recovered - previousRecovered,
            "deceased": deceased - previousDeceased,
            "total": 0,
            "tested": 0
        },
        "total": {
            "confirmed": confirmed,
            "probable": 0,
            "recovered": recovered,
            "deceased": deceased,
            "total": 0,
            "tested": 0
        }
    }
    previousConfirmed = confirmed
    previousRecovered = recovered
    previousDeceased = deceased

print(timeseries['TT'])
# Construct output JSON
with open('./processed/timeseries.min.json', 'w', encoding='utf-8') as f:
    json.dump(timeseries, f, ensure_ascii=False, indent=4)

# Construct data.json, which holds current figures for each region.
data = {}

today_df = pd.read_csv('./overview_today.csv')
previousConfirmed = 0
previousDeceased = 0
previousRecovered = 0

for index, row in today_df.iterrows():
    region = row['Region']
    data[region] = {
        "delta": {
            "confirmed": 0,
            "deceased": 0,
            "recovered": 0,
        },
        "meta": {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+12:00"),#"2020-08-16T22:17:52+05:30",
            "population": 99999,
            "tested": {
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d"),#"2020-08-13",
                "source": ""
            } 
        },
        "total": {
            "confirmed": row['Confirmed'],
            "deceased": row['Deceased'],
            "recovered": row['Confirmed'] - row['Deceased'],
            "probably": row['Probable'],
            "tested": 0,
            "Incidence rate (per 100 000)":  row['Incidence rate (per 100 000)']
        }
    }

with open('./processed/data.min.json', 'w', encoding='utf-8') as d:
    json.dump(data, d, ensure_ascii=False, indent=4)



'''
1. Create the dataset
2. Save the dataset to the DB
3. Rewire API call to load the data in the same format into timeseries.
4. Automate new data using Github Actions

'''

