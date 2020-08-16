# https://nzcoviddashboard.esr.cri.nz/#!/
# Processing the CSV files 
# Save all of this data into DB

# Separately scrape or update the site on a daily basis.
import pandas as pd
import datetime
import json

# df = pd.read_csv('./covid_19_data_portal.csv')
# df = pd.read_csv('./covid-cases-Confirmed.csv')
# df = pd.read_csv('./jhhs_confirmed.csv')
df = pd.read_csv('overview_dhb.csv')
print(df.head(10))
print(df.columns)
data = {}
def createDatesForDHB(df):
    # print(df['Region'].values[0])
    region = df['Region'].values[0]

    data[region] = {
        "dates": {}
    }
    for index, row in df.iterrows():
        # print(date)
        date = row['Date']
        data[region]['dates'][date] = {
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
# print(df.describe())
# print(df.head(10))
# print(df.columns)
for i, g in df.groupby('Region'):
    createDatesForDHB(g)

# Group dataframe into regions
# print(data)
with open('./processed/timeseries.min.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
# print(df['Region'].unique())
# Extract all historical data as timeseries data

# Construct output JSON



'''
1. Create the dataset
2. Save the dataset to the DB
3. Rewire API call to load the data in the same format into timeseries.

'''

