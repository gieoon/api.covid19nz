# Create data for different dates at endpoints
# e.g. /processed/data-2020-08-20.min.json
# For now just create for NZ nationwide

import pandas as pd
import datetime

confirmed_df = pd.read_csv('./jhhs_nz_confirmed.csv')
recovered_df = pd.read_csv('./jhhs_nz_recovered.csv')
deaths_df = pd.read_csv('./jhhs_nz_recovered.csv')

def getNZRow(df):
    return df.loc[df['Country/Region'] == 'New Zealand']


data = {}

previousConfirmed = 0
previousDeceased = 0
previousRecovered = 0

population_df = pd.read_csv('./dhb_populations.csv')

def getPopulation(region):
    # print(region)
    if region == 'Mid Central':
        region = 'Midcentral'
    if region == 'Tairāwhiti':
        region = 'Tairawhiti'
    if region == 'Waitematā':
        region = 'Waitemata'
    return int(population_df.loc[population_df['Region'] == region]['Population'].values[0])


def createData(date, filename, previousConfirmed, previousDeceased, previousRecovered):
    # with open('./processed/days/data-' + )
    data['TT'] = {
        "delta": {
            "confirmed": getNZRow(confirmed_df)[date].values[0] - previousConfirmed,
            "deceased": getNZRow(deaths_df)[date].values[0] - previousDeceased,
            "recovered": getNZRow(recovered_df)[date].values[0] - previousRecovered,
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
            "confirmed": getNZRow(confirmed_df)[date].values[0],
            "deceased": getNZRow(deaths_df)[date].values[0],
            "recovered": getNZRow(recovered_df)[date].values[0],
            # "tested": getTestedCount(region),
        }
    }
    previousConfirmed = getNZRow(confirmed_df)[date].values[0]
    previousDeceased = getNZRow(deaths_df)[date].values[0]
    previousRecovered = getNZRow(recovered_df)[date].values[0]

# Loop through each date and save as new file
for date in confirmed_df.columns[4:]:
    print("date: ", date)
    dateObj = datetime.strptime(date, '%m/%d/%y')
    filename = datetime.strftime(dateObj, 'yy-&m-%d')
    print("filename: ", filename)
    # Create filename from date in YY-mm-dd format
    createData(date, filename, previousConfirmed, previousDeceased, previousRecovered)
