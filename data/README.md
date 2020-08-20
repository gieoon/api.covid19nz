# Scraping instructions

1. Run update.sh script, which runs main.py and all scrapers
2. Scrape https://nzcoviddashboard.esr.cri.nz/#!/ , click on 'View Data', and download CSV, 
3. Save as __'overview_today.csv'__
4. Scrape https://nzcoviddashboard.esr.cri.nz/#!/, scroll down to 'Case Curve' and click on 'View Data', 'Download CSV'
5. Go to John Hopkins and get historical data for recovered, confirmed, deceased separately
6. Append to timeseries data
7. Save as __'timeseries_dhb/csv'__ 
8. Scrape https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases,
Get the date this was last updated and store it in runtime memory as variable.
9. Save as __'overview_daily.csv'__
10. Use Github Actions to automatically push this data using SSH credentials.