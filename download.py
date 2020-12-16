import os
import calendar
import csv

FX_RATES_URL = "https://gist.githubusercontent.com/ger-f/f4701ce5dad91f13028cd6ebfc740ba7/raw/181f764da55cb5bcbd2c6a65f4b412665bf3f2b5/csv"
RATES_FILE = "rates.csv"
REVENUE_URL = "https://gist.githubusercontent.com/ger-f/0fd94e0cac53ab5e393fdc20dd40e8e1/raw/421744b058df6e727e9c8fb5915dc9d80a6b0f69/revenue.csv"
REVENUE_FILE = "revenue.csv"

def downloadFile (url, file_name, number_of_tries):
    #attempts to download the requested file 
    try:
        os.system(f"wget -O -tries={number_of_tries} {file_name} {url} && echo {file_name} downloaded")
        return True
    except:
        print("{} could not be downloaded.".format(file_name))
        return False

def fxRatesParser (file_name, currencies = [], all_currencies = False):
    #gets the fx rates for the requested currencies
    with open(file_name, 'r') as fo:
        reader = csv.reader(fo, delimiter=',')
        header = next(reader)
        print(header)
        if all_currencies:
            currencies = header[1:]
            return dailyRates(reader, header, currencies)
        elif len(currencies) == 0:
            raise Exception("No currencies have been chosen.")
        else:
            return dailyRates(reader, header, currencies)

def dailyRates (csv_file, header, currencies):
    #prepares the daily rates and adds to the fx_rates dictionary
    fx_rates = {}
    for row in csv_file: 
        daily_rates = {}  
        for currency in currencies:
            daily_rates.update({currency : row[header.index(currency)]})
        fx_rates.update({row[header.index('Date')]: daily_rates})
           
    return fx_rates

def convertedRevenue (file_name, fx_rates, currency):
    #Calculates de converted revenue, currently just prints the results
    converted_revenue = []

    with open(file_name, "r") as fo:
        csv_file = csv.reader(fo, delimiter=',')
        for row in csv_file:
            date = row[0]
            euro_revenue = (row[1] + ','+ row[2]).replace('"','')
            revenue = euro_revenue[2:].replace(',', "")
            month = list(calendar.month_abbr).index(date.split()[0])
            lookup_key = f"{date.split()[2]}-{month if int(month)>10 else '0'+str(month)}-{date.split()[1]}"
            try:
                converted_revenue.append(float(revenue) * float(fx_rates[lookup_key][currency]))
            except:
                print("skipping weekend day")

    print(f"Converted currency to {currency} for {len(converted_revenue)} days")
    print(converted_revenue)
    

"""MAIN"""
downloadFile(FX_RATES_URL, RATES_FILE, 10)
downloadFile(REVENUE_URL, REVENUE_FILE, 10)
fx_rates = fxRatesParser(RATES_FILE, currencies = ['SEK', 'GBP', 'USD'])
print(f'found rates for {len(fx_rates)} days')
convertedRevenue(REVENUE_FILE, fx_rates, 'SEK')

