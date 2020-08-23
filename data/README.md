# Scraping instructions

1. Run update.sh script, which runs main.py and all scrapers
2. Scrape https://nzcoviddashboard.esr.cri.nz/#!/ , click on 'View Data', and download CSV, 
3. Save as __'overview_today.csv'__
4. Scrape https://nzcoviddashboard.esr.cri.nz/#!/, scroll down to 'Case Curve' and click on 'View Data', 'Download CSV'
5. Save as __'timeseries_dhb.csv'__
6. Go to John Hopkins and get historical data for recovered, confirmed, deceased separately
https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv

https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv

https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv

7. Save these to __jhhs_nz_confirmed.csv__, __jhhs_nz_deaths.csv__, __jhhs_nz_recovered.csv__ respectively.
8. Scrape https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases,
Get the date this was last updated and store it in runtime memory as variable.
9. Save as __'overview_daily.csv'__
10. Run main.py to create new updates
11. Create a new updates file 
12. Save to 
13. Use Github Actions to automatically push this data using SSH credentials.


# Regional data
Bay of Plenty testing data
https://covid19.bopdhb.govt.nz/

Nelson Marlborough testing data
https://www.nmdhb.govt.nz/quicklinks/about-us/emergency-management-and-planning/covid-19/covid-19-testing-data
